from django.db import models
from datetime import datetime
from o3gm.models import O3gmPoint
from sensorium.models import UploadIp, GPSLocationSensor, RadioSensor, DeviceInfoSensor, BatterySensor
from django.contrib.gis.geos import Point
import logging

log = logging.getLogger('transform')

class SensoriumToO3gm(models.Model):
  
  save_timestamp = models.DateTimeField()
  num_points = models.IntegerField(max_length=8) 

  def transform(self):
    '''
    Transforms Sensorium Sensor data to O3gm Points.
    Assumes that Sensorium Sensors with same save_timestamp belong to each other.
    The transformation uses GPSLocationSensor records as base for O3gm Points.
    For every other Sensor it uses the record whith the same save_timestamp and the first smaller capture_timestamp
    than the GPS LocationSensor record.
    
    The SensoriumToO3gm object assigns its attributes and saves itself in this method
    (actually this should be a constructor)
    '''
    
    self.save_timestamp = datetime.now()
    self.num_points = 0
    
    # Has there been a transformation before
    try:
      last_trans = SensoriumToO3gm.objects.latest('save_timestamp')
    except:
      # If not retrieve all GPS records, which were saved befor this transformation now
      # with Longitude and Latitude Data 
      gps_location_qs = GPSLocationSensor.objects.filter(
                              save_timestamp__lt=self.save_timestamp, privacy_level='1'
                            ).exclude(longitude__isnull=True, latitude__isnull=True
                            ).exclude(longitude='n/a', latitude='n/a')
          
                            
    else:
      # Retrieve GPS records, like above but saved after last transformation
      gps_location_qs = GPSLocationSensor.objects.filter(
                              save_timestamp__gte=last_trans.save_timestamp, privacy_level='1'
                            ).filter(
                              save_timestamp__lt=self.save_timestamp
                            ).exclude(longitude__isnull=True, latitude__isnull=True
                            ).exclude(longitude='n/a', latitude='n/a')
                            
    # Create O3gm point for every GPS record like so: 
    for gps_location in gps_location_qs:
      point = O3gmPoint()
      # All points of this transformation will have the same save_timestamp
      point.save_timestamp = self.save_timestamp
      
      # Assign GPSLocationSensor attributes to O3gm point
      point.capture_timestamp = gps_location.capture_timestamp
      point.alt               = gps_location.altitude
      point.geometry          = Point(float(gps_location.longitude), float(gps_location.latitude))
      point.accuracy          = gps_location.accuracy
      
      
      # Check if there exists an IP record for the GPS record and assign
      # If there only should exist one
      try:
        upload_ip = UploadIp.objects.filter(save_timestamp=gps_location.save_timestamp)[0]
      except Exception, e:
        pass # Is this worth logging?
      else:
        point.ip = upload_ip.ip
                             
      # Retrieve Radio records for the record 
      # that have been captured earlier than the GPS record
      # in descending order by there capture_timestamp              
      radio_qs = RadioSensor.objects.all().filter(
                              save_timestamp=gps_location.save_timestamp
                              ).filter(
                              capture_timestamp__lte=gps_location.capture_timestamp
                              ).filter(privacy_level='1'
                              ).order_by('-capture_timestamp')

      # Assign closest (save_timestamp) property from Radio records to O3gm point
      # Can be different for each property 
      for radio_record in radio_qs:
        if point.mcc and point.mnc and point.lac and point.cell_id and point.nw_type and point.rssi:
          break
        if not point.mcc and radio_record.mcc:
          point.mcc = radio_record.mcc
        if not point.mnc and radio_record.mnc:
          point.mnc = radio_record.mnc
        if not point.lac and radio_record.lac:
          point.lac = radio_record.lac
        if not point.cell_id and radio_record.cell_id:
          point.cell_id = radio_record.cell_id
        if not point.nw_type and radio_record.nw_type:
          point.nw_type = radio_record.nw_type
        if not point.rssi and radio_record.rssi:
          point.rssi = radio_record.rssi
      
      if not point.mcc or not point.mnc or not point.lac or not point.cell_id or not point.nw_type or not point.rssi:
        continue
          
      # Same as above for Radio Sensor 
      device_qs = DeviceInfoSensor.objects.filter(
                              save_timestamp=gps_location.save_timestamp
                              ).filter(
                              capture_timestamp__lte=gps_location.capture_timestamp
                              ).filter(privacy_level='1'
                              ).order_by('-capture_timestamp')       
        
      for device_record in device_qs:
        if point.tac and point.vendor and point.model:
          break
        
        if not point.tac and device_record.tac:
          point.tac = device_record.tac
        if not point.vendor and device_record.vendor:
          point.vendor = device_record.vendor
        if not point.model and device_record.model:
          point.model = device_record.model

      # Same as above for Radio Sensor
      battery_qs = BatterySensor.objects.filter(
                              save_timestamp=gps_location.save_timestamp
                              ).filter(
                              capture_timestamp__lte=gps_location.capture_timestamp
                              ).filter(privacy_level='1'
                              ).order_by('-capture_timestamp')
                            
      for battery_record in battery_qs:
        if point.battery_level:
          break
        
        if not point.battery_level and battery_record.charged:
          point.battery_level = battery_record.charged
          
      # If point is safed successfully, increment point counter
      try:
        point.save()
      except Exception, e:
        log.error(e)
      else:
        self.num_points += 1
        
    self.save()
