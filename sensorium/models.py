from django.db import models
from datetime import datetime

def val(rec, key):
  try:
    if (rec[key] == 'n/a'):
      raise
    else:
      return rec[key]
  except:
    return None

class UploadIp(models.Model):
  save_timestamp = models.DateTimeField()
  ip             = models.TextField(null=True)
  
  
class Sensor(models.Model):
  capture_timestamp = models.DateTimeField(null=True)
  save_timestamp    = models.DateTimeField()
  privacy_level     = models.IntegerField(max_length=2)
  
  def create(self, save_ts, rec):
    self.save_timestamp = save_ts 
    
    privacy = val(rec, 'privacy-level')
    
    if privacy == "NO":
      self.privacy_level = 1
    elif privacy == "LOW":
      self.privacy_level = 2
    elif privacy == "MED":
      self.privacy_level = 3
    elif privacy == "HIGH":
      self.privacy_level = 4
    elif privacy == "FULL":
      self.privacy_level = 5
    else:
      self.privacy_level = privacy
    
    try:
      self.capture_timestamp = datetime.fromtimestamp(float(rec['timestamp']) / 1000.0)
    except:
      self.capture_timestamp = None 
  
  class Meta:
    abstract = True

class BatterySensor(Sensor):
  charged      = models.TextField(null=True)
  power_source = models.TextField(null=True)
  battery_type = models.TextField(null=True)
  temperature  = models.TextField(null=True)
  voltage      = models.TextField(null=True)
  
  def create(self, save_ts, rec):
    super(BatterySensor, self).create(save_ts, rec)
    self.charged      = val(rec, 'charged')
    self.power_source = val(rec, 'power source')
    self.battery_type = val(rec, 'battery type')
    self.temperature  = val(rec, 'temperature')
    self.voltage      = val(rec, 'voltage')

class DeviceInfoSensor(Sensor):
  available_memory = models.TextField(null=True)
  cpu_usage        = models.TextField(null=True)
  low_memory_th    = models.TextField(null=True)
  model            = models.TextField(null=True)
  vendor           = models.TextField(null=True)
  tac              = models.TextField(null=True)
  total_memory     = models.TextField(null=True)
  android_vers     = models.TextField(null=True)

  def create(self, save_ts, rec):
    super(DeviceInfoSensor, self).create(save_ts, rec)
    self.available_memory = val(rec, 'available memory')
    self.cpu_usage        = val(rec, 'CPU usage')
    self.low_memory_th    = val(rec, 'low memory threshold')
    self.model            = val(rec, 'model')
    self.vendor           = val(rec, 'vendor')
    self.tac              = val(rec, 'TAC')
    self.total_memory     = val(rec, 'total memory')
    self.android_vers     = val(rec, 'android version')

class LocationSensor(Sensor):
  accuracy  = models.TextField(null=True)
  altitude  = models.TextField(null=True)
  latitude  = models.TextField(null=True)
  longitude = models.TextField(null=True)
  speed     = models.TextField(null=True)
    
  def create(self, save_ts, rec):
    super(LocationSensor, self).create(save_ts, rec)
    self.accuracy  = val(rec, 'accuracy')
    self.altitude  = val(rec, 'altitude')
    self.latitude  = val(rec, 'latitude')
    self.longitude = val(rec, 'longitude')
    self.speed     = val(rec, 'speed')
    
  class Meta:
    abstract = True
    
class GPSLocationSensor(LocationSensor):
  satellites = models.TextField(null=True)
  bearing    = models.TextField(null=True)
  address    = models.TextField(null=True)

  
  def create(self, save_ts, rec):
    super(GPSLocationSensor, self).create(save_ts, rec)
    self.satellites = val(rec, 'satellites')
    self.bearing    = val(rec, 'bearing')
    self.address    = val(rec, 'address')
    
    
class NetworkLocationSensor(LocationSensor):
  address = models.TextField(null=True)

  def create(self, save_ts, rec):
    super(NetworkLocationSensor, self).create(save_ts, rec)
    self.address = val(rec, 'address')
    
  
class RadioSensor(Sensor):
  cell_id     = models.TextField(null=True)
  lac         = models.TextField(null=True)
  mcc         = models.TextField(null=True)
  mnc         = models.TextField(null=True)
  nw_type     = models.TextField(null=True)
  operator    = models.TextField(null=True)
  roaming     = models.TextField(null=True)
  radio_state = models.TextField(null=True)
  rssi        = models.TextField(null=True)
  subscriber  = models.TextField(null=True)
  
  def create(self, save_ts, rec):
    super(RadioSensor, self).create(save_ts, rec)
    self.cell_id     = val(rec, 'cell id')
    self.lac         = val(rec, 'location area code')
    self.mcc         = val(rec, 'mobile country code')
    self.mnc         = val(rec, 'mobile network code')
    self.nw_type     = val(rec, 'network type')
    self.operator    = val(rec, 'operator')
    self.roaming     = val(rec, 'roaming')
    self.radio_state = val(rec, 'radio state')
    self.rssi        = val(rec, 'received signal strength')
    self.subscriber  = val(rec, 'subscriber id')
    
    
class WifiConnectionSensor(Sensor):
  link_speed       = models.TextField(null=True)
  supplicant_state = models.TextField(null=True)
  bssid            = models.TextField(null=True)
  mac              = models.TextField(null=True)
  device_ip        = models.TextField(null=True)
  rssi             = models.TextField(null=True)
  ssid_hidden      = models.TextField(null=True)
  ssid             = models.TextField(null=True)
  
  def create(self, save_ts, rec):
    super(WifiConnectionSensor, self).create(save_ts, rec)
    self.link_speed       = val(rec, 'link speed')
    self.supplicant_state = val(rec, 'Supplicant State')
    self.bssid            = val(rec, 'BSSID')
    self.mac              = val(rec, 'MAC address')
    self.device_ip        = val(rec, 'device IP')
    self.rssi             = val(rec, 'received signal strength')
    self.ssid_hidden      = val(rec, 'SSID hidden')
    self.ssid             = val(rec, 'SSID')

class BluetoothSensor(Sensor):
  scanned_devs = models.TextField(null=True)
  dev_name     = models.TextField(null=True)
  mac_addr     = models.TextField(null=True)
  bonded_devs  = models.TextField(null=True)
  
  def create(self, save_ts, rec):
    super(BluetoothSensor, self).create(save_ts, rec)
    self.scanned_devs = val(rec, 'scanned device(s)')
    self.dev_name     = val(rec, 'device name')
    self.mac_addr     = val(rec, 'MAC address')
    self.bonded_devs  = val(rec, 'bonded device(s)')

class WifiSensor(Sensor):
  dev_ip       = models.TextField()
  
  def create(self, save_ts, rec):
    super(WifiSensor, self).create(save_ts, rec)
    self.dev_ip = val(rec, 'device IP')





