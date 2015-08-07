$(document).ready(function(){

    var networkDict = {
        "GSM" : "#CC0000","GPRS" : "#FF0000","EDGE" : "#FF7F00","2G/3G" : "#FEE034","UMTS" : "#FFFF00","HSPA" : "#7FFF00","HSDPA" : "#00FF00","HSPA+" : "#00FF7F","3G/4G"  : "#00FFFF","LTE" : "#3366FF","LAN" : "#990099","WLAN" : "#660066"
    };
  

    /*
     * Create legend
     */
    var legend = document.getElementById('color-info');
    for (var key in networkDict) {
        var canvas_container = document.createElement('span');
        canvas_container.setAttribute('class', 'canvas-container');
        legend.appendChild(canvas_container);

        var canvas = document.createElement('canvas');
        canvas_container.appendChild(canvas);

        canvas.setAttribute('id', key + '-canvas');
        canvas.setAttribute('width', "22px");
        canvas.setAttribute('height', "20px");
        var context = canvas.getContext('2d');
        context.beginPath();
        context.arc(10, 12, 8, 0, 2 * Math.PI, false);
        context.fillStyle = networkDict[key];
        context.fill();

        var tag = document.createElement('label');
        tag.setAttribute('for', key + '-canvas');
        tag.setAttribute('class', "canvas-label");
        tag.innerHTML = key;
        canvas_container.appendChild(tag);
    }
     

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