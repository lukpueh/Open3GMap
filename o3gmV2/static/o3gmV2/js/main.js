$(document).ready(function(){
    /*
     * Setup Map and tile server
     */
    var map = L.map('map').setView([48.2, 16.367], 1);
    L.tileLayer(
        'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>' +
                     'contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
        }).addTo(map);


    /*
     * Get Points from Server
     */
    
    $.get('/o3gmv2/point_json/',  function(data){
        var points = data; 

        var markers = L.markerClusterGroup();

        for (var i = 0; i < points.length; i++) {
            var point = points[i];
            var marker = L.marker(new L.LatLng(point[3], point[2]), { title: point[1] });
            marker.bindPopup(point[1]);
            markers.addLayer(marker);
        }


        map.addLayer(markers);
    });

});