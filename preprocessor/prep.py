# open data file
# 
# create geojson objects from lines
# 
# create cell objects
# with points from each according line
# with attributes from each according line

import jarvismarch
import geojson
import csv
import math
  
fileName = "../data/o3gmreadings121212.txt"
data = csv.DictReader(open(fileName), delimiter=" ", quotechar="'")

pointFeatureArray = []
polygonPoints = {
  "cells" : {},
  "lacs" : {}
}

def lon_to_merc(lon):
  return float(lon) * 20037508.34 / 180
  
def lat_to_merc(lat):
  y = float(lat)
  y = math.log(math.tan( (90 + y) * math.pi / 360)) / (math.pi / 180)
  return 20037508.34 * y / 180
  
def add_polygon_point(name, id, point):
  try:
    polygonPoints[name][id]
  except:
    polygonPoints[name][id] = []
  finally:
    polygonPoints[name][id].append(point)


for row in data:
  # Create Points
  x = lon_to_merc(row["lon"])
  y = lat_to_merc(row["lat"])
  point = [x, y]
  
  # Create Point Features
  geoJsonPoint = geojson.Point(point)
  geoJsonFeature = geojson.Feature(geometry=geoJsonPoint, properties=row)
  pointFeatureArray.append(geoJsonFeature)
  
  # create point collections for cells
  add_polygon_point("cells", row["cell_id"], point)
  
  
  # create point collections for lacs
  if (row["lac"] != "UnknownLAC"):
    add_polygon_point("lacs", row["lac"], point)
    
cellFeatureArray = []
#CellFeature
for cell, points in polygonPoints["cells"].iteritems(): 
  if (len(points) >= 3):
    coordinates = jarvismarch.convex_hull(points)
    coordinates.append(coordinates[0])
    geoJsonPolygon = geojson.Polygon([coordinates])
    geoJsonFeature = geojson.Feature(geometry=geoJsonPolygon,
                                    properties={"cell_id" : cell})
    cellFeatureArray.append(geoJsonFeature)

lacFeatureArray = []
for lac, points in polygonPoints["lacs"].iteritems(): 
  if (len(points) >= 3):
    coordinates = jarvismarch.convex_hull(points)
    coordinates.append(coordinates[0])
    geoJsonPolygon = geojson.Polygon([coordinates])
    geoJsonFeature = geojson.Feature(geometry=geoJsonPolygon,
                                    properties={"lac" : lac})
    lacFeatureArray.append(geoJsonFeature)



pointCollection = geojson.FeatureCollection(pointFeatureArray)
cellCollection = geojson.FeatureCollection(cellFeatureArray)
lacCollection = geojson.FeatureCollection(lacFeatureArray)


 
f = open("../data/points.json", 'w')
f.write(geojson.dumps(pointCollection))
f = open("../data/cells.json", 'w')
f.write(geojson.dumps(cellCollection))
f = open("../data/lac.json", 'w')
f.write(geojson.dumps(lacCollection))



