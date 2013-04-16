import os, sys, csv
from datetime import datetime
from django.contrib.gis.geos import Point
from models import O3gmPoint

                        

def save_csv(path):
  '''Iterates over a list of
  dictionaries. Each dictionary is potentially
  a o3gm Point.
  returns count of successfully created points
  '''
  rd = csv.DictReader(open(path), 
                        delimiter=" ", quotechar="'")
  save_ts = datetime.now()
  
  for o3gm_dict in rd:
    point = O3gmPoint()
    
    point.save_timestamp = save_ts
      
    try:  
      point.capture_timestamp = datetime.fromtimestamp(float(o3gm_dict['timestamp']) / 1000.0)
    except Exception as e:
      print "capture_timestamp", e
    
    try:  
      point.mcc =  o3gm_dict['mcc']
    except Exception as e:
      print "mcc", e
    
    try:  
       point.mnc =  o3gm_dict['mnc']
    except Exception as e:
      print "mnc", e

    try:  
      point.lac = o3gm_dict['lac']
    except Exception as e:
      print "lac", e

    try:  
      point.cell_id = o3gm_dict['cell_id'] 
    except Exception as e:
      print "cell_id", e
    
    try:  
      point.nw_type = o3gm_dict['nw_type']
    except Exception as e:
      print "nw_type", e
    
    try:  
      point.rssi = o3gm_dict['rssi']
    except Exception as e:
      print "rssi", e
        
    try:  
      point.loc_source = o3gm_dict['loc_source']  
    except Exception as e:
      print "locsource", e
    
    try:  
      point.alt = o3gm_dict['alt']
    except Exception as e:
      print "alt", e
    
    try:  
      point.accuracy = o3gm_dict['accuracy']
    except Exception as e:
      print "accuracy", e
    
    try:  
      point.battery_level = o3gm_dict['battery_level']  
    except Exception as e:
      print "battery_level", e
    
    try:  
      point.tac = o3gm_dict['tac']
    except Exception as e:
      print "tac", e
    
    try:  
      point.vendor = o3gm_dict['vendor']
    except Exception as e:
      print "vendor", e
    
    try:  
      point.model = o3gm_dict['model'] 
    except Exception as e:
      print "model", e
    
    try:  
      point.ip = o3gm_dict['ip']
    except Exception as e:
      print "ip", e
    
    try:  
      point.geometry = Point(float(o3gm_dict['lon']), float(o3gm_dict['lat']))
    except Exception as e:
      print "geometry", e

    try:
      point.save()
    except Exception as e:
      print o3gm_dict
      print "not saved", e
    
