from django.contrib import admin
from models import RTRNetztest

class RTRNetztestAdmin(admin.ModelAdmin):
  list_display = ('open_uuid','time','cat_technology','network_type','lat','long','loc_src','zip_code','download_kbit','upload_kbit','ping_ms','signal_strength','server_name','test_duration','num_threads','plattform','model','client_version','network_mcc_mnc','network_name','sim_mcc_mnc','connection','asn','ip_anonym','ndt_download_kbit','ndt_upload_kbit')
  
admin.site.register(RTRNetztest, RTRNetztestAdmin)


