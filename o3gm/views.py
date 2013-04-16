from vectorformats.Formats import Django, GeoJSON
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse
from o3gm import models
import json

def _convert_to_json(queryset, properties):
  djf = Django.Django(geodjango='geometry', properties=properties)
  geoj = GeoJSON.GeoJSON()
  return geoj.encode(djf.decode(queryset))
  

point_properties = [ 'mcc', 'mnc' ,  'lac', 'cell_id', 'nw_type', 'rssi',  
                     'alt', 'accuracy', 'battery_level', 'tac', 'vendor', 'model', 'ip' ]

cell_properties = [ 'cell_id', 'prevailing_nw_type', 'prevailing_nw_count' ]
lac_properties = [ 'lac', 'prevailing_nw_type', 'prevailing_nw_count' ]

  
def serve_point_json(request):
  
  if (request.method == 'OPTIONS'):
    return HttpResponse(status=200)

  if (request.method == 'GET'):
    try:
      bbox = request.GET.get('bbox').split(',')
      geom = Polygon.from_bbox(bbox)
    except:
      return HttpResponse(status='400')
    else:
      queryset = models.O3gmPoint.objects.filter(geometry__contained=geom)
      return HttpResponse(_convert_to_json(queryset, point_properties), content_type='application/json')
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
  