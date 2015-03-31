from django.conf.urls import patterns, include, url


urlpatterns = patterns('o3gmV2.views',
    url(r'^$', 'index'),
    url(r'^point_json/', 'serve_point_json', name='serve_point_json'),

)
