from django.conf.urls import patterns, include, url

urlpatterns = patterns('sensorium.views',
    url(r'^$', 'upload_files', name='upload_files'),
)
