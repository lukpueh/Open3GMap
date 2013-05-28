from django.contrib.gis import admin
from models import O3gmPoint, O3gmCell, O3gmLac


def normalize_decimal(value):
  return value.normalize()

class O3gmPointAdmin(admin.GeoModelAdmin):
  list_display = ('save_timestamp', 'data_source', 'mcc', 'mnc', 'lac', 'cell_id', 'nw_type', 'rssi', 'loc_source', 'alt', 'accuracy', 'battery_level', 'tac', 'vendor', 'model', 'ip')

class O3gmCellAdmin(admin.GeoModelAdmin):
  list_display = ('save_timestamp', 'cell_id', 'prevailing_nw_type', 'prevailing_nw_count')
  
class O3gmLacAdmin(admin.GeoModelAdmin):
  list_display = ('save_timestamp', 'lac', 'prevailing_nw_type', 'prevailing_nw_count')
  
admin.site.register(O3gmPoint, O3gmPointAdmin)
admin.site.register(O3gmCell, O3gmCellAdmin)
admin.site.register(O3gmLac, O3gmLacAdmin)