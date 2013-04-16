from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponse
from datetime import datetime
import models
import os
import json
import logging


log = logging.getLogger('sensorium')

@csrf_exempt
def upload_files(request):
  '''
  This function receives a post request, with multiple files.
  checks user
  checks datatype multipart (json)
  creates a datetime for this upload session
  if a model exits for the file,
  calls a function that saves all json files to the database
  '''
  #o3gm_upload_user
  #o3gm_upload_user_password
  

  if (request.method == 'POST'):
    # try:
    #   username = str(request.POST['username'])
    #   password = str(request.POST['password'])
    #   user = authenticate(username=username, password=password)
    # except Exception as err:
    #   log.error("No username and password specified" + str(err))  
    #   return HttpResponse(status=400)
      
    # if user is not None:
    save_ts = datetime.now()
      
    try:
      ip = request.META['REMOTE_ADDR']
      upload_ip = models.UploadIp()
      log.info("File Upload from: " + ip)
      upload_ip.save_timestamp = save_ts
      upload_ip.ip = ip
      upload_ip.save()
    except Exception as err:
      log.error(str(err))
      

    for file_name, uploaded_file in request.FILES.iteritems():
      
      try:
        file_name = os.path.basename(str(file_name))
      except:
        file_name = "default"
        
      try:
      	# Save to file 
        save_name = save_ts.strftime('%Y%m%d%H%M%S%f') + file_name
        save_as_file(uploaded_file, save_name)
      except Exception, e:
        log.error(e)
        
      # try:
      #   log.info(file_name)
      #   json_data = json.load(uploaded_file.seek(0))
      # except Exception as err:
      #   log.error(str(err))
      # else:
      #   try:
      #     save_json_file(save_ts, json_data, file_name)
      #   except Exception as err:
      #     log.error(str(err))
      
    return HttpResponse(status=200)
      
    # log.info("Could not authenticate with: " + username + " and " + password)  
    # return HttpResponse(status=400)
    
  log.info("Wrong request method " + str(request.method))
  return HttpResponse(status=400)
  
def save_as_file(uploaded_file, name):
  path = '/home/puehringer/openlayers/sensorium/uploaded_files/'
  
  # if the file exists, another timestamp is added to the name
  try:
    with open(path + name) as f: pass
    name = name + datetime.now().strftime('%Y%m%d%H%M%S%f')
  except:
    pass
    
  with open(path + name, 'wb+') as destination:
    for chunk in uploaded_file.chunks():
      destination.write(chunk)

    
def save_local_files():
  '''
  feed uploaded jsonfiles to sensorium database
  '''  
  abspath = '/Users/topfpflanze/source/openlayers/sensorium/uploaded_files'
  for root, dirs, files in os.walk(abspath):    
    for file_name in files:
      try:
        file_data = open(os.path.join(abspath, file_name), "r")
        save_ts_str = file_name[:20] 
        save_ts = datetime.strptime(save_ts_str, '%Y%m%d%H%M%S%f') # convert to datetime
        file_name_strip = file_name[20:]
        save_json_file(save_ts, json.load(file_data), file_name_strip)
      except Exception, e:
        log.error(file_name)
        log.exception(e)

        
      file_data.close()
  
def save_json_file(save_ts, json_file, name):
  
  for record in json_file:
    if (record["privacy-level"] == 0 or record["privacy-level"] == "NO"):
      pr = True # no privacy
    else:
      pr = False   
    
    if (name == "BatterySensor.json"):
      sensor = models.BatterySensor() if pr else models.BatterySensorPr()
    elif (name == "DeviceInfoSensor.json"):
      sensor = models.DeviceInfoSensor() if pr else models.DeviceInfoSensorPr()
    elif (name == "GPSLocationSensor.json"):
      sensor = models.GPSLocationSensor() if pr else models.GPSLocationSensorPr()
    elif (name == "NetworkLocationSensor.json"):
      sensor = models.NetworkLocationSensor() if pr else models.NetworkLocationSensorPr()
    elif (name == "RadioSensor.json"):
      sensor = models.RadioSensor() if pr else models.RadioSensorPr()
    else:
      break

    try:
      sensor.assign_record(save_ts, record)
      sensor.save()
    except Exception, e:
      log.error(str(record)) 
      log.exception(e)

      
save_json_file.transactions_per_request = False