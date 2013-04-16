



import os, json
from sensorium import models
from datetime import datetime

path = "/Users/topfpflanze/source/openlayers/sensorium/uploaded_files"

def sanatize_json(file_data):
  try:
    file_str = file_data.read()
    json_data = json.loads(file_str + "[]")
  except Exception, e:
    print e
    return False
  else:
    #print "succefully appended ]"
    return json_data


def save_json(save_ts, json_file, name):  
  
  for record in json_file:
    if (name == "BatterySensor.json"):
      sensor = models.BatterySensor() 
    elif (name == "DeviceInfoSensor.json"):
      sensor = models.DeviceInfoSensor() 
    elif (name == "GPSLocationSensor.json"):
      sensor = models.GPSLocationSensor() 
    elif (name == "NetworkLocationSensor.json"):
      sensor = models.NetworkLocationSensor() 
    elif (name == "RadioSensor.json"):
      sensor = models.RadioSensor()
    elif (name == "WifiConnectionSensor.json"):
      sensor = models.WifiConnectionSensor() 
    elif (name == "WifiSensor.json"):
      sensor = models.WifiSensor()
    elif (name == "BluetoothSensor.json"):
      sensor = models.BluetoothSensor() 
    else:
      break

    try:
      sensor.create(save_ts, record)
      sensor.save()
    except Exception, e:
      print record, e
      
      


for root, dirs, files in os.walk(path):
  for fn in files:
    try:
      file_data = open(os.path.join(path, fn), "r")
      save_ts = datetime.strptime(fn[:20], '%Y%m%d%H%M%S%f')
      file_name = fn[20:]
    except Exception, e:
      print fn, e
    else:
      try:
        json_data = json.load(file_data)
      except:
        json_data = sanatize_json(file_data)
        
      if json_data:
        try:
          save_json(save_ts, json_data, file_name)
        except Exception, e:
          print fn, e
      
      file_data.close()
      