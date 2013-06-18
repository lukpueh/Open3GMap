from vectorformats.Formats import Django, GeoJSON
from django.contrib.gis.geos import Polygon
from django.shortcuts import render
from django.http import HttpResponse
from o3gm import models
import json
import os, json, logging
from django.contrib.gis.geos import Point


log = logging.getLogger('o3gm')


def _convert_to_json(queryset, properties):
  djf = Django.Django(geodjango='geometry', properties=properties)
  geoj = GeoJSON.GeoJSON()
  return geoj.encode(djf.decode(queryset))
  

point_properties = [ 'mcc', 'mnc' ,  'lac', 'cell_id', 'nw_type', 'rssi',  
                     'alt', 'accuracy', 'battery_level', 'tac', 'vendor', 'model', 'ip' ]

cell_properties = [ 'cell_id', 'prevailing_nw_type', 'prevailing_nw_count' ]
lac_properties = [ 'lac', 'prevailing_nw_type', 'prevailing_nw_count' ]



def index(request):
  context = {
    'nw_types' : [nw_type.encode('ascii', 'replace') for nw_type in models.O3gmPoint.objects.exclude(nw_type__isnull=True).values_list('nw_type', flat=True).distinct()],
    'operators' : [operator for operator in models.O3gmPoint.objects.exclude(mnc__isnull=True, mcc__isnull=True).values_list('mcc', 'mnc').distinct()]
  }
  
  return render(request, 'o3gm/index.html', context)
  
  
def serve_point_json(request):
  
  if (request.method == 'OPTIONS'):
    return HttpResponse(status=200)

  if (request.method == 'GET'):
    
    tmp= models.O3gmPoint.objects.all()
    tmp= models.O3gmPoint.objects.filter(data_source="RTR").distinct('geometry')
    qs = models.O3gmPoint.objects.all()
    qs = models.O3gmPoint.objects.filter(data_source="RTR").distinct('geometry')
    
    # #bounding box
    try:
      bbbox = request.GET.get('bbox').split(',')
      # print bbbox
      # geom = Polygon.from_bbox(bbbox)
      # qs   = qs.filter(geometry__contained=geom)
      #print len (qs)
    except Exception, e:
      log.error(e)
      

    fact = 10
    bboxes = []
    left = float(bbbox[0])
    bottom = float(bbbox[1])
    right = float(bbbox[2])
    top = float(bbbox[3])
    x_len = (right - left) / fact
    y_len = (top - bottom) / fact
    
    for y in range(0, fact):
      for x in range(0, fact):
        bboxes.append({
          'left': left + x_len * x,
          'bottom': bottom + y_len * y,
          'right': left + x_len * (x + 1),
          'top': bottom + y_len * (y + 1),
        })
        
    qs = []
    for bb in bboxes:
      point = models.O3gmPoint()
      point.geometry = Point(bb['left'], bb['bottom'])
      qs.append(point)
    
    
    cnt = 0
    for bb in bboxes:
      cnt += 1
      geom = Polygon.from_bbox([ bb['left'], bb['bottom'], bb['right'], bb['top'] ])
      tmp1   = tmp.filter(geometry__contained=geom)
      print cnt, "# ", len(tmp1)
      
    # operator
    #     try:
    #       mcc, mnc = request.GET.get('operator').split(',')
    #       qs = qs.filter(mcc=int(mnc), mnc=int(mcc))
    #     except Exception, e:
    #       log.error(e)
      
    #network type 
    # try:
    #   nw_type = str(request.GET.get('nw_type'))
    #   
    #   if (nw_type == "none"):
    #     qs = qs.filter(nw_type__isnull=True)
    #   elif (nw_type == "all" ):
    #     pass
    #   else:
    #     qs = qs.filter(nw_type=nw_type)
    # except Exception, e:
    #   log.error(e)
    
    try:
      print len(qs)
      json_data = _convert_to_json(qs, point_properties)
    except Exception, e:
      log.error(e)
    else:
      return HttpResponse(json_data, content_type='application/json')
      
  return HttpResponse(status='400')

def serve_cell_json(request):
  queryset = models.O3gmCell.objects.all()
  return HttpResponse(_convert_to_json(queryset, cell_properties), content_type='application/json')

def serve_lac_json(request):
  queryset = models.O3gmLac.objects.all()
  return HttpResponse(_convert_to_json(queryset, lac_properties), content_type='application/json')


def serve_point_json_file(request):
  queryset = models.O3gmPoint.objects.all()
  response = HttpResponse(_convert_to_json(queryset, point_properties), content_type='application/octet-stream')
  response['Content-Disposition'] = 'attachment; filename="points.json"'
  return response
  
def serve_cell_json_file(request):
  queryset = models.O3gmCell.objects.all()
  response = HttpResponse(_convert_to_json(queryset, cell_properties), content_type='application/octet-stream')
  response['Content-Disposition'] = 'attachment; filename="cells.json"'
  return response

def serve_lac_json_file(request):
  queryset = models.O3gmLac.objects.all()
  response = HttpResponse(_convert_to_json(queryset, lac_properties), content_type='application/octet-stream')
  response['Content-Disposition'] = 'attachment; filename="lacs.json"'
  return response
  