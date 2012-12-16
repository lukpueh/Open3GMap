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
cellDict = {}

for row in data:
  # PointFeatures
  x = float(row["lon"]) * 20037508.34 / 180
  y = math.log(math.tan( (90 + float(row["lat"])) * math.pi / 360)) / (math.pi / 180)
  y = 20037508.34 * y / 180;
  
  point = [x, y]
  geoJsonPoint = geojson.Point(point)
  geoJsonFeature = geojson.Feature(geometry=geoJsonPoint, properties=row)
  pointFeatureArray.append(geoJsonFeature)
  
  # Cells
  cell = str(row["cell_id"])
  try:
    cellDict[cell]
  except:
    cellDict[cell] = []
  finally:
    cellDict[cell].append(point)
  
  
cellFeatureArray = []
#CellFeature
for cell, points in cellDict.iteritems(): 
  if (len(points) >= 3):
    coordinates = jarvismarch.convex_hull(points)
    coordinates.append(coordinates[0])
    geoJsonPolygon = geojson.Polygon([coordinates])
    geoJsonFeature = geojson.Feature(geometry=geoJsonPolygon,
                                    properties={"cell_id" : cell})
    cellFeatureArray.append(geoJsonFeature)
                      


pointCollection = geojson.FeatureCollection(pointFeatureArray)
cellCollection = geojson.FeatureCollection(cellFeatureArray)

 
f = open("points.json", 'w')
f.write(geojson.dumps(pointCollection))
f = open("cells.json", 'w')
f.write(geojson.dumps(cellCollection))

