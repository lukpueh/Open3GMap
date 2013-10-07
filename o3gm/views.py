from vectorformats.Formats import Django, GeoJSON
from django.contrib.gis.geos import Polygon
from django.shortcuts import render
from django.http import HttpResponse
from o3gm import models
import os, json, logging
from django.contrib.gis.geos import Point

log = logging.getLogger('o3gm')

# point_properties  = [ 'mcc', 'mnc', 'lac', 'cell_id', 'nw_type', 'rssi',  
#                       'accuracy', 'battery_level', 'tac', 'vendor', 'model', 'ip' ]
point_properties  = [ 'id', 'nw_type' ]
cell_properties   = [ 'cell_id', 'prevailing_nw_type', 'prevailing_nw_count' ]
lac_properties    = [ 'lac', 'prevailing_nw_type', 'prevailing_nw_count' ]

def _convert_geodjango_to_json(queryset, properties):
  djf = Django.Django(geodjango='geometry', properties=properties)
  geoj = GeoJSON.GeoJSON()
  return geoj.encode(djf.decode(queryset))

# def _gridify_bbox(bbox, fact_v = 20, fact_h = 30):
#   '''
#   Take Bounding Box array and make a grid of it.
#   parameters:
#     bbox [<left-lon>, <bottom-lat>, <right-lon>, <top-lat>]
#   return:
#     array of bboxes
#   '''
#    
#   bboxes = []
#   left   = float(bbox[0])
#   bottom = float(bbox[1])
#   right  = float(bbox[2])
#   top    = float(bbox[3])
#   
#   x_len  = (right - left) / fact_h
#   y_len  = (top - bottom) / fact_v
#   
#   for y in range(0, fact_v):
#     for x in range(0, fact_h):
#       bboxes.append([
#         left + x_len * x,
#         bottom + y_len * y,
#         left + x_len * (x + 1),
#         bottom + y_len * (y + 1)
#       ])
#         
#   return bboxes

def _data_options_context(data_src):
  
  qs_nw_types = models.O3gmPoint.objects.all()
  qs_operators = models.O3gmPoint.objects.all()
  
  if (data_src == "S"):
    qs_nw_types = qs_nw_types.exclude(data_source='R')
    qs_operators = qs_operators.exclude(data_source='R')
  elif (data_src == "R"): 
    qs_nw_types = qs_nw_types.filter(data_source='R')
    qs_operators = qs_operators.filter(data_source='R')  
  
  
  qs_nw_types = qs_nw_types.exclude(nw_type__isnull=True
                           ).values_list('nw_type', flat=True
                           ).distinct()
  qs_operators =  qs_operators.exclude(mnc__isnull=True, mcc__isnull=True
                           ).values_list('mcc', 'mnc'
                           ).order_by('mcc').distinct()
                            
  return {
    'nw_types' : [nw_type.encode('ascii', 'replace') for nw_type in qs_nw_types],
    'operators' : [operator for operator in qs_operators]
  }

def index(request):
  return render(request, 'o3gm/index.html', _data_options_context("S"))
  
def data_options(request):
  data_src = request.GET.get('data_src')
  return render(request, 'o3gm/options.html', _data_options_context(data_src))
  
def serve_point_properties(request):
  point_id = request.GET.get('point_id')
  context = { 'point' : models.O3gmPoint.objects.filter(id=point_id)[0] }
  return render(request, 'o3gm/point_properties.html', context)
  
def serve_point_json(request):
  
  if (request.method == 'OPTIONS'):
    return HttpResponse(status=200)

  if (request.method == 'GET'):
    
    qs = models.O3gmPoint.objects.distinct('geometry')
    
    # BOUNDING BOX
    try:
      bbox = request.GET.get('bbox').split(',')
      print bbox
      geom = Polygon.from_bbox(bbox)
      qs    = qs.filter(geometry__contained=geom)
    except Exception, e:
      log.error(e)
      
    # bboxes = _gridify_bbox(bbbox)
    # grid_tuples = []
    # abox = Polygon.from_bbox(bboxes[0])
 
    # for bb in bboxes:
    #   geom_bb = Polygon.from_bbox(bb)
    #   qs_bb = models.O3gmPoint.objects.filter(geometry__contained=geom_bb)
    #   qs_bb_num = len(qs_bb)
    #   if (qs_bb_num):
    #     grid_tuples.append( { "geometry": geom_bb.json } )
      
       
    #     
    #   qs_bbox = models.O3gmPoint.objects.filter(geometry__contained=geom)
    #   qs_bbox_len = len(qs_bbox)
    #   if (qs_bbox_len):
    #     print cnt, "# ", len(qs_bbox)
    
    # SELECT DATA SOURCE
    try:
      data_source = str(request.GET.get('data_source'))
      print data_source
      if (data_source == "R"):
        qs = qs.filter(data_source="R")
      else:
        qs = qs.exclude(data_source="R")
    except Exception, e:
      log.error(e)
      
    # SELECT OPERATOR
    try:
      operator = request.GET.get('operator')
      print operator
      if (str(operator) != "all"):
        mcc, mnc = operator.split(',')
        qs = qs.filter(mcc=int(mcc), mnc=int(mnc))
    except Exception, e:
      log.error(e)
      
    # SELECT NETWORK TYPE
    try:
      nw_type = str(request.GET.get('nw_type'))
      print nw_type
      if (nw_type != "all" ):
        if (nw_type == "none"):
          qs = qs.filter(nw_type__isnull=True)
        else:
          qs = qs.filter(nw_type=nw_type)
    except Exception, e:
      log.error(e)
    
    try:
      print len(qs)
      json_data = _convert_geodjango_to_json(qs, point_properties)
    except Exception, e:
      log.error(e)
    else:
      return HttpResponse(json_data, content_type='application/json')
      
  return HttpResponse(status='400')

def serve_cell_json(request):
  qs = models.O3gmCell.objects.all()
  try:
    bbox = request.GET.get('bbox').split(',')
    geom = Polygon.from_bbox(bbox)
    qs    = qs.filter(geometry__intersects=geom)
  except Exception, e:
    log.error(e)
  return HttpResponse(_convert_geodjango_to_json(qs, cell_properties), content_type='application/json')

def serve_lac_json(request):
  qs = models.O3gmLac.objects.all()
  try:
    bbox = request.GET.get('bbox').split(',')
    geom = Polygon.from_bbox(bbox)
    qs    = qs.filter(geometry__intersects=geom)
  except Exception, e:
    log.error(e)
  return HttpResponse(_convert_geodjango_to_json(qs, lac_properties), content_type='application/json')


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
  