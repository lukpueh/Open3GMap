from django.conf.urls import patterns, include, url

urlpatterns = patterns('o3gm.views',
    url(r'^$', 'index'),
    url(r'^data_options/', 'data_options'),
    url(r'^point_properties/', 'serve_point_properties'),
    url(r'^point_json/', 'serve_point_json', name='serve_point_json'),
    url(r'^cell_json/', 'serve_cell_json', name='serve_cell_json'),
    url(r'^lac_json/', 'serve_lac_json', name='serve_lac_json'),
    url(r'^point_json_file/', 'serve_point_json_file', name='serve_point_json_file'),
    url(r'^cell_json_file/', 'serve_cell_json_file', name='serve_cell_json_file'),
    url(r'^lac_json_file/', 'serve_lac_json_file', name='serve_lac_json_file'),
)
