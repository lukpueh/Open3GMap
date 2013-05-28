from django.db import models

# Create your models here.

class RTRNetztest(models.Model):
  open_uuid         = models.CharField(max_length=56, null=True) 
  time              = models.DateTimeField(null=True) #2012-12-22 13:27 UTC timestamp to_timestamp(input, 'YYYY-MM-DD HH:MI')
  cat_technology    = models.CharField(max_length=16, null=True)
  network_type      = models.CharField(max_length=16, null=True)
  lat               = models.DecimalField(max_digits=32, decimal_places=24, null=True) 
  long              = models.DecimalField(max_digits=32, decimal_places=24, null=True) 
  loc_src           = models.CharField(max_length=16, null=True)
  zip_code          = models.IntegerField(max_length=16, null=True)
  download_kbit     = models.IntegerField(max_length=16, null=True)
  upload_kbit       = models.IntegerField(max_length=16, null=True)
  ping_ms           = models.DecimalField(max_digits=32, decimal_places=24, null=True)
  signal_strength   = models.IntegerField(max_length=16, null=True)
  server_name       = models.CharField(max_length=16, null=True)
  test_duration     = models.IntegerField(max_length=16, null=True)
  num_threads       = models.IntegerField(max_length=16, null=True)
  plattform         = models.CharField(max_length=16, null=True)
  model             = models.CharField(max_length=56, null=True)
  client_version    = models.CharField(max_length=16, null=True)
  network_mcc_mnc   = models.CharField(max_length=16, null=True)
  network_name      = models.CharField(max_length=32, null=True)
  sim_mcc_mnc       = models.CharField(max_length=16, null=True)
  connection        = models.CharField(max_length=32, null=True)
  asn               = models.IntegerField(max_length=16, null=True)
  ip_anonym         = models.CharField(max_length=56, null=True)
  ndt_download_kbit = models.IntegerField(max_length=16, null=True)
  ndt_upload_kbit   = models.IntegerField(max_length=16, null=True)
  
