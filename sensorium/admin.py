from django.contrib import admin
import models


class UploadIpAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'ip')
    
class BatterySensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'charged', 'power_source', 'battery_type', 'temperature', 'voltage')

class DeviceInfoSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'available_memory', 'cpu_usage', 'low_memory_th', 'model', 'vendor', 'tac', 'total_memory', 'android_vers')
  
class GPSLocationSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'accuracy', 'altitude', 'latitude', 'longitude', 'speed', 'satellites', 'bearing', 'address')
  
class NetworkLocationSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'accuracy', 'altitude', 'latitude', 'longitude', 'speed', 'address')

class RadioSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'cell_id', 'lac', 'mcc', 'mnc', 'nw_type', 'operator', 'roaming', 'radio_state', 'rssi', 'subscriber')

class WifiConnectionSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'link_speed', 'supplicant_state', 'bssid', 'mac', 'device_ip', 'rssi', 'ssid_hidden', 'ssid')

class BluetoothSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'scanned_devs', 'dev_name', 'mac_addr', 'bonded_devs')
  
class WifiSensorAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'capture_timestamp', 'privacy_level', 'dev_ip')
       
  
admin.site.register(models.UploadIp, UploadIpAdmin)
admin.site.register(models.BatterySensor, BatterySensorAdmin)
admin.site.register(models.DeviceInfoSensor, DeviceInfoSensorAdmin)
admin.site.register(models.GPSLocationSensor, GPSLocationSensorAdmin)
admin.site.register(models.NetworkLocationSensor, NetworkLocationSensorAdmin)
admin.site.register(models.RadioSensor, RadioSensorAdmin)

admin.site.register(models.WifiConnectionSensor, WifiConnectionSensorAdmin)
admin.site.register(models.BluetoothSensor, BluetoothSensorAdmin)
admin.site.register(models.WifiSensor, WifiSensorAdmin)

