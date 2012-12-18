import jarvismarch
import geojson
import csv
import math
import os
import sys

class Container:
  def __init__(self):
    self.points = []
    self.cells = {}
    self.lacs = {}

  def create_points(self, file_name):
    data = csv.DictReader(open(file_name), delimiter=" ", quotechar="'")
    for row in data:
      self.points.append(Point(row["lon"], row["lat"], row))
  
  def create_cells(self):
    for point in self.points:
      id = point.properties["cell_id"]
      if (id not in self.cells):
        self.cells[id] = Cell()
      self.cells[id].points.append(point)
    for cell in self.cells.values():
      cell.create_linear_ring()
      cell.create_properties()
      
  def create_lacs(self):
    for point in self.points:
      id = point.properties["lac"]
      if (id != "UnknownLAC"):
        if (id not in self.lacs):
          self.lacs[id] = Lac()
        self.lacs[id].points.append(point)
    for lac in self.lacs.values():
      lac.create_linear_ring()
      lac.create_properties()
    
  def create_feature_collections(self, path):
    self._write_feature_collection(self.points, path+"points.json")
    self._write_feature_collection(self.cells.values(), path+"cells.json")
    self._write_feature_collection(self.lacs.values(), path+"lacs.json")
    
  def _write_feature_collection(self, list, file_name):
    feature_collection = []
    for item in list:
      feature_collection.append(item.get_feature())
    f = open(file_name, 'w')
    f.write(geojson.dumps(geojson.FeatureCollection(feature_collection)))
    

class Point:
  def __init__(self, lon, lat, properties):
    self.coordinates = [self.lon_to_merc(lon), self.lat_to_merc(lat)]
    self.properties = properties
    
  def lon_to_merc(self, lon):
    return float(lon) * 20037508.34 / 180
  
  def lat_to_merc(self, lat):
    y = float(lat)
    y = math.log(math.tan( (90 + y) * math.pi / 360)) / (math.pi / 180)
    return 20037508.34 * y / 180
    
  def get_feature(self):
    return geojson.Feature(geometry=geojson.Point(self.coordinates),\
                            properties=self.properties)
  
class Polygon:
  def __init__(self):
    self.points = []
    self.ring = []
    self.properties = {}
    
  def create_linear_ring(self):
    coordinates = []
    for point in self.points:
      coordinates.append(point.coordinates)
    self.ring = jarvismarch.convex_hull(coordinates)
    self.ring.append(self.ring[0])
  
  def get_feature(self):
    return geojson.Feature(geometry=geojson.Polygon([self.ring]),\
                            properties=self.properties) 

class Cell(Polygon):
  def __init__(self):
    Polygon.__init__(self)
  
  def create_properties(self):
    
    self.properties["cell_id"] = self.points[0].properties["cell_id"]
    self.properties["lac"] = "UnknownLAC"

    for point in self.points:
      if (point.properties["lac"] != "UnknownLAC"):
        self.properties["lac"] = point.properties["lac"]
        break
        
    # create list of netwerk types and a prevalent network type
    nw_type_dict = {}
    for point in self.points:
      nw_type = point.properties["nw_type"]
      if (nw_type not in nw_type_dict):
        nw_type_dict[nw_type] = 0
      nw_type_dict[nw_type] += 1
      
    self.properties["nw_types"] = nw_type_dict
    count_max = max(nw_type_dict.itervalues())
    pnts = []
    for nw_type, count in nw_type_dict.iteritems():
      if count == count_max:
        pnts.append(nw_type)

    self.properties["pnt"] = pnts[0]
    # if (len(pnts) == 1):
    #   self.properties["pnt"] = pnts[0]
    # else:
    #   # take best out of list
    #   print pnts        

class Lac(Polygon):
  def __init__(self):
    Polygon.__init__(self)
  
  def create_properties(self):
    self.properties["lac"] = self.points[0].properties["lac"] 
  
###############
##MAIN PROGRAMM

# Create Points and write Point featurecollection


path = "../data/"

try:
  filename = sys.argv[1]
  os.path.exists(filename)
except:
  print "USAGE: python "+sys.argv[0]+" <filename>"
  sys.exit(2)

if not os.path.exists(path):
    os.makedirs(path)

container = Container()
container.create_points(filename)
container.create_cells()
container.create_lacs()
container.create_feature_collections(path)

  

  



    
