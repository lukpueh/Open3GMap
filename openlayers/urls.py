from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sensorium/', include('sensorium.urls')),
    url(r'^o3gm/', include('o3gm.urls'))
)
