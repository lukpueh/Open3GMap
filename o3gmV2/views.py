from vectorformats.Formats import Django, GeoJSON
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from o3gm import models
import json, logging

log = logging.getLogger('o3gm')

def index(request):
    return render(request, 'o3gmV2/index.html',{})

def serve_point_json(request):
  
    if (request.method == 'OPTIONS'):
        return HttpResponse(status=200)

    if (request.method == 'GET'):
        qs = models.O3gmPoint.objects.distinct('geometry').values('id', 'nw_type', 'geometry')[:10]
        result = [[point['id'], str(point['nw_type']), point['geometry'].x, point['geometry'].y] for point in qs]
        return HttpResponse(json.dumps(result), content_type='application/json')

    return HttpResponse(status='400')
      
    
