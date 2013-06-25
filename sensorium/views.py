from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponse
from datetime import datetime
import models
import os, json, logging


log = logging.getLogger('sensorium')

@csrf_exempt
def upload_files(request):
  '''
  This function receives a post request, with multiple files.
  checks datatype multipart (json)
  creates a datetime for this upload session
  if a model exits for the file,
  calls a function that saves all json files to the database
  '''
  
  if (request.method == 'POST'):
    save_ts = datetime.now()
      
    try:
      ip = request.META['REMOTE_ADDR']
      upload_ip = models.UploadIp()
      log.info("File Upload from: " + str(ip))
      upload_ip.save_timestamp = save_ts
      upload_ip.ip = ip
      upload_ip.save()
    except Exception, e:
      log.error(str(e))
      

    for file_name, file_handler in request.FILES.iteritems():
      try:
        file_name = os.path.basename(str(file_name))
      except:
        file_name = "default"
      
      if (file_handler.size > 10000000):
        log.info("File '" + str(file_name) + "' too big: " + str(file_handler.size))
        continue
        
      json_data = get_valid_json(file_handler)
      
      if json_data:
        try:
          save_json_to_model(save_ts, json_data, file_name)
        except Exception, e:
          log.error(str(e))

      
    return HttpResponse(status=200)   
    
  log.info("Wrong request method: " + str(request.method))
  return HttpResponse(status=400)

  
def save_json_to_model(save_ts, json_file, name):
  
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
      log.error(str(record)) 
      log.error(e)


def get_valid_json(file_handler):
  try:
    file_str = ''
    for chunk in file_handler.chunks():
      file_str += chunk
    return json.loads(file_str)
  except Exception, e:
    try:
      json_data = json.loads(file_str + "]")
      return json_data
    except:
      return False
      
    
def load_json_from_fs(path):
  for root, dirs, files in os.walk(path):
    for fn in files:
      try:
        file_handler = open(os.path.join(path, fn), "r")
        save_ts = datetime.strptime(fn[:20], '%Y%m%d%H%M%S%f')
        file_name = fn[20:]
      except Exception, e:
        log.error(e)
      else:
        json_data = get_valid_json(file_handler)

        if json_data:
          try:
            save_json_to_model(save_ts, json_data, file_name)
          except Exception, e:
            log.error(e)

        file_handler.close()