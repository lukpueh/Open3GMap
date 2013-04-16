from itertools import groupby
from django.contrib.gis.geos import MultiPoint
from o3gm import models
from datetime import datetime


def assign_polygons(code_name, key_func):
  

  sorted_points = models.O3gmPoint.objects.order_by(code_name)
  
  grouped_points = {}
  for code, points_iterator in groupby(sorted_points, key_func):
	  grouped_points[code] = list(points_iterator)
  
  for code, points in grouped_points.iteritems():
    #only consider cells with more than two points in it
    if (len(points) > 2) and code:
      try:
        if code_name == 'cell_id':
          polygon = models.O3gmCell()
          polygon.cell_id = code
        elif code_name == 'lac':
          polygon = models.O3gmLac()
          polygon.lac = code
        else:
          pass

        mp = MultiPoint([ p.geometry for p in points ])
        polygon.save_timestamp = datetime.now()
        polygon.geometry = mp.convex_hull
        polygon.set_prevailing_nw_type()
        polygon.save()
      except Exception as err:
    	  print err
    	  
    	  
# Delete all polygon objects from table 
try:
  models.O3gmCell.objects.all().delete()
  models.O3gmLac.objects.all().delete()
except Exception as err:
  print err
else:
  print "Deleted Polygon Objects"

# Create new polygons (cells and lacs)
assign_polygons('cell_id', lambda point: point.cell_id)
assign_polygons('lac', lambda point: point.lac)




  	  
  	  
