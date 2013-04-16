from django.contrib.gis.db import models
from django.db.models import Count

class O3gmPoint(models.Model):
  
  save_timestamp = models.DateTimeField()
  capture_timestamp = models.DateTimeField(null=True)
  mcc = models.IntegerField(max_length=4, null=True)
  mnc = models.IntegerField(max_length=4, null=True)
  lac = models.CharField(max_length=16, null=True)
  cell_id = models.IntegerField(max_length=16, null=True)
  nw_type = models.CharField(max_length=16, null=True)
  rssi = models.DecimalField(max_digits=32, decimal_places=16, null=True)
  loc_source = models.CharField(max_length=8, null=True)
  alt = models.DecimalField(max_digits=32, decimal_places=16, null=True)
  accuracy = models.DecimalField(max_digits=32, decimal_places=16, null=True)
  battery_level = models.DecimalField(max_digits=32, decimal_places=16, null=True)
  tac = models.IntegerField(max_length=16, null=True)
  vendor = models.CharField(max_length=16, null=True)
  model = models.CharField(max_length=16, null=True)
  ip = models.CharField(max_length=16, null=True)

  geometry = models.PointField(srid=4326)
  objects = models.GeoManager()
  

class O3gmPolygon(models.Model):
  
  save_timestamp = models.DateTimeField()
  prevailing_nw_type = models.CharField(max_length=16, null=True)
  prevailing_nw_count = models.IntegerField(max_length=16, null=True)
  geometry = models.PolygonField(srid=4326)
  objects = models.GeoManager()
  
  class Meta:
    abstract = True
    
  def set_prevailing_nw_type(self, queryset):
    '''
    take a list of points.
    find pnt
    '''
    try:
      q = queryset.values('nw_type')
      q = q.annotate(Count('nw_type'))
      pnt = q.order_by('-nw_type__count')[0]
      self.prevailing_nw_type = pnt['nw_type']
      self.prevailing_nw_count = pnt['nw_type__count']
    except Exception as err:
      pass
      # I want some logging here
    
    
class O3gmCell(O3gmPolygon):
  cell_id = models.IntegerField(max_length=10, null=True)
  
  def set_prevailing_nw_type(self):
    queryset = O3gmPoint.objects.filter(cell_id=self.cell_id)
    super(O3gmCell, self).set_prevailing_nw_type(queryset)

class O3gmLac(O3gmPolygon):
  lac = models.IntegerField(max_length=10, null=True)
  
  def set_prevailing_nw_type(self):
    queryset = O3gmPoint.objects.filter(lac=self.lac)
    super(O3gmLac, self).set_prevailing_nw_type(queryset)


  
    