from vectorformats.Formats import Django, WKT, GeoJSON
from django.contrib.gis.geos import Polygon
from django.shortcuts import render
from django.http import HttpResponse
from o3gm import models
import os, json, logging
from django.contrib.gis.geos import Point

log = logging.getLogger('o3gm')

point_properties  = [ 'mcc', 'mnc', 'lac', 'cell_id', 'nw_type', 'rssi',  
                      'accuracy', 'battery_level', 'tac', 'vendor', 'model', 'ip' ]
cell_properties   = [ 'cell_id', 'prevailing_nw_type', 'prevailing_nw_count' ]
lac_properties    = [ 'lac', 'prevailing_nw_type', 'prevailing_nw_count' ]

def _convert_geodjango_to_json(queryset, properties):
  djf = Django.Django(geodjango='geometry', properties=properties)
  geoj = GeoJSON.GeoJSON()
  return geoj.encode(djf.decode(queryset))

def _gridify_bbox(bbox, fact_v = 20, fact_h = 30):
  '''
  Take Bounding Box array and make a grid of it.
  parameters:
    bbox [<left-lon>, <bottom-lat>, <right-lon>, <top-lat>]
  return:
    array of bboxes
  '''
   
  bboxes = []
  left   = float(bbox[0])
  bottom = float(bbox[1])
  right  = float(bbox[2])
  top    = float(bbox[3])
  
  x_len  = (right - left) / fact_h
  y_len  = (top - bottom) / fact_v
  
  for y in range(0, fact_v):
    for x in range(0, fact_h):
      bboxes.append([
        left + x_len * x,
        bottom + y_len * y,
        left + x_len * (x + 1),
        bottom + y_len * (y + 1)
      ])
        
  return bboxes


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
    
    qs = models.O3gmPoint.objects.exclude(data_source="R").distinct('geometry')
    
    # #bounding box
    try:
      bbbox = request.GET.get('bbox').split(',')
      # qs   = qs.filter(geometry__contained=geom)
    except Exception, e:
      log.error(e)
      
    bboxes = _gridify_bbox(bbbox)
    grid_tuples = []
 
    for bb in bboxes:
      geom_bb = Polygon.from_bbox(bb)
      qs_bb = models.O3gmPoint.objects.filter(geometry__contained=geom_bb)
      qs_bb_num = len(qs_bb)
      if (qs_bb_num):
        grid_tuples.append( geom_bb.json )
       
    #     
    #   qs_bbox = models.O3gmPoint.objects.filter(geometry__contained=geom)
    #   qs_bbox_len = len(qs_bbox)
    #   if (qs_bbox_len):
    #     print cnt, "# ", len(qs_bbox)
      
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
      #print len(qs)
      #json_data = _convert_geodjango_to_json(qs, point_properties)
      # djf = Django.Django(pickled_geometry=True)
      # djf.decode(bboxes_geom)
      json_data = grid_tuples
      print grid_tuples
    except Exception, e:
      log.error(e)
    else:
      return HttpResponse(json_data, content_type='application/json')
      
  return HttpResponse(status='400')

def serve_cell_json(request):
  queryset = models.O3gmCell.objects.all()
  res = _convert_geodjango_to_json(queryset, cell_properties)
  print res 
  return HttpResponse( content_type='application/json')

def serve_lac_json(request):
  queryset = models.O3gmLac.objects.all()
  return HttpResponse(_convert_geodjango_to_json(queryset, lac_properties), content_type='application/json')


def serve_point_json_file(request):
  queryset = models.O3gmPoint.objects.all()
  response = HttpResponse(_convert_geodjango_to_json(queryset, point_properties), content_type='application/octet-stream')
  response['Content-Disposition'] = 'attachment; filename="points.json"'
  return response
  
def serve_cell_json_file(request):
  queryset = models.O3gmCell.objects.all()
  response = HttpResponse(_convert_geodjango_to_json(queryset, cell_properties), content_type='application/octet-stream')
  response['Content-Disposition'] = 'attachment; filename="cells.json"'
  return response

def serve_lac_json_file(request):
  queryset = models.O3gmLac.objects.all()
  response = HttpResponse(_convert_geodjango_to_json(queryset, lac_properties), content_type='application/octet-stream')
  response['Content-Disposition'] = 'attachment; filename="lacs.json"'
  return response
  