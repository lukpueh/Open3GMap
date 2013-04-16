import os, json

path = "/Users/topfpflanze/source/openlayers/sensorium/uploaded_files"

f = {
"BatterySensor.json" :  {},
"BluetoothSensor.json" : {},
"DeviceInfoSensor.json" : {},
"GPSLocationSensor.json" : {},
"NetworkLocationSensor.json" : {},
"RadioSensor.json" : {},
"WifiConnectionSensor.json" :{},
"WifiSensor.json" : {}
}


def append_brack(file_data):
  try:
    file_str = file_data.read()
    json_data = json.loads(file_str + "[]")
  except Exception, e:
    print e
    return False
  else:
    #print "succefully appended ]"
    return json_data

for root, dirs, files in os.walk(path):
  for fn in files:
    try:
      file_data = open(os.path.join(path, fn), "r")
      file_name = fn[20:]
    except Exception, e:
      print fn, e
    else:
      try:
        json_data = json.load(file_data)
      except:
        json_data = append_brack(file_data)
        
      if json_data:
        for record in json_data:
          if (record["privacy-level"] == 0 or record["privacy-level"] == "NO"):
            for key, val in record.iteritems():
              try:
                if (len(val) > len(f[file_name][key])):
                  f[file_name][key] = val
              except:
                f[file_name][key] = val
      
      file_data.close()

for key, value in f.iteritems():
  for k, v in f[key].iteritems():
    f[key][k] = str(v.encode('ascii','replace')) + " ## " + str(len(v))
  
print f