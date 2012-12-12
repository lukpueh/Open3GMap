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

fileName = "../data/o3gm_readings.txt.latest"
data = csv.DictReader(open(fileName), delimiter=" ")

pointFeatureArray = []
cellDict = {}

for row in data:
  # PointFeatures
  point = [float(row["lon"]), float(row["lat"])]
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

 
f = open(fileName + ".points.json", 'w')
f.write(geojson.dumps(pointCollection))
f = open(fileName + ".cells.json", 'w')
f.write(geojson.dumps(cellCollection))

