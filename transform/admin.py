from django.contrib import admin
import models

class RtrToO3gmAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'num_points')

class SensoriumToO3gmAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'num_points')
  
class O3gmPointToO3gmPolygonsAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'num_cells', 'num_lacs')

admin.site.register(models.RtrToO3gm, RtrToO3gmAdmin)
admin.site.register(models.SensoriumToO3gm, SensoriumToO3gmAdmin)
admin.site.register(models.O3gmPointToO3gmPolygons, O3gmPointToO3gmPolygonsAdmin)