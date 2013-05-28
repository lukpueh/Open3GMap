from vectorformats.Formats import Django, GeoJSON
from django.contrib.gis.geos import Polygon
from django.shortcuts import render
from django.http import HttpResponse
from o3gm import models
import json
import os, json, logging


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
    
    #qs = models.O3gmPoint.objects.all()
    qs = models.O3gmPoint.objects.filter(data_source="RTR").distinct('geometry')
    
    # #bounding box
    # try:
    #   bbox = request.GET.get('bbox').split(',')
    #   geom = Polygon.from_bbox(bbox)
    #   qs   = qs.filter(geometry__contained=geom)
    # except Exception, e:
    #   log.error(e)
      
    #operator
    # try:
    #   mcc, mnc = request.GET.get('operator').split(',')
    #   qs = qs.filter(mcc=int(mnc), mnc=int(mcc))
    # except Exception, e:
    #   log.error(e)
      
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
  