from django.core.management import setup_environ 
from open3gmap import settings 
setup_environ(settings)

from transform.models import SensoriumToO3gm, O3gmPointToO3gmPolygons

try: 
  print "Starting Points transformation"
  points = SensoriumToO3gm()
  points.transform()
except Exception, e:
  print e

try: 
  print "Starting Polys transformation"
  polys = O3gmPointToO3gmPolygons()
  polys.transform()
except Exception, e:
  print e
