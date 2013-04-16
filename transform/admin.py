from django.contrib import admin
import models


class SensoriumToO3gmAdmin(admin.ModelAdmin):
  list_display = ('save_timestamp', 'num_points')
  

admin.site.register(models.SensoriumToO3gm, SensoriumToO3gmAdmin)