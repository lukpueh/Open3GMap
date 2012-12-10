var map;
var layer_mapnik;
var layers_object;
var network_color = {
  GPRS : "#FF0000",
  EDGE : "#FF7F00",
  UMTS : "#FFFF00",
  HSPA : "#7FFF00",
  HSUPA : "#00FF00",
  HSDPA : "#00FF7F",
  HSPAP : "#00FFFF"
};

function init_map() {
  var map_lon = 16.355, map_lat = 48.22;
  var map_zoom = 13;
  
  map = new OpenLayers.Map('map');
  layer_mapnik = new OpenLayers.Layer.OSM("Mapnik");
  map.addLayer(layer_mapnik);
  map.setCenter(
    new OpenLayers.LonLat(_lon2merc(map_lon), _lat2merc(map_lat)), map_zoom);
  
  layers_object = {}; 
  
  map.addControl(new OpenLayers.Control.KeyboardDefaults());
  
  // event handler control
  $(document).on('change', '.control-check', function(e) {
    var layer =  layers_object[e.target.value];
    layer.getVisibility() ? layer.setVisibility(0) : layer.setVisibility(1);
  });
  
  
  $.get('points.php', function(data, status){
    $.each($.parseJSON(data), function(key,val){
        draw_point_feature(val.nw_type, val.lon, val.lat, val);
      });
  });
  
  $.get('cells.php', function(data, status){
    $.each($.parseJSON(data), function(key,val){
        draw_cell_feature("all", val, {"Cell id" : val[0].cell_id});
      });
  });
  
  //create_select_control();
}

function _get_layer(layer_type, layer_id) {
  if (!layers_object.hasOwnProperty(layer_id)) {
    
    //create the new layer
    layers_object[layer_id] = new OpenLayers.Layer.Vector(layer_type+" "+layer_id);
    map.addLayer(layers_object[layer_id]);
    
    //add layer show/hide handle
    $('#controls').append("<input \
      class='control-check' \
      type='checkbox' \
      value='"+layer_id+"' \
      checked='checked'> \
      "+layer_id+" "+layer_type+"<br>");
    
    create_select_control()
    }
  return layers_object[layer_id];

}

function draw_point_feature(layer_ID, x, y, attributes) {
  // get layer
  var layer = _get_layer("points", layer_ID);      
  // style
  var style_point = {
    fillColor: network_color[attributes.nw_type],
    strokeWidth: 0,
    pointRadius: 7
  }; 
  // creates new feature with point
  // appends feature to the layer 
  var feature = new OpenLayers.Feature.Vector(
    new OpenLayers.Geometry.Point(
      _lon2merc(parseFloat(x)), 
      _lat2merc(parseFloat(y))
    ), attributes, style_point);

  layer.addFeatures(feature);
}

function draw_cell_feature(layer_ID, point_array, attributes) {
  
  var layer = _get_layer("cells", layer_ID);  
  //creates new feature with polygon
  //appends polygon to the layer
  var ring = new OpenLayers.Geometry.LinearRing();
  
  for (var i= 0; i < point_array.length; i++) {
    ring.addComponent(new OpenLayers.Geometry.Point(
      _lon2merc(parseFloat(point_array[i].lon)), 
      _lat2merc(parseFloat(point_array[i].lat))
      )
    );
  }
  var feature = new OpenLayers.Feature.Vector(
    new OpenLayers.Geometry.Polygon(ring), attributes);
  layer.addFeatures(feature);
}


function create_select_control() {
  // hack, can't use layers_object to pass to selectfeature, need layers_array
  layers_array = new Array();
  for (layer in layers_object) {
    layers_array.push(layers_object[layer]);
  }
  var select_ctrl = new OpenLayers.Control.SelectFeature(layers_array, {
      hover: true,
      onSelect: function(feature){
        var feature_div = document.getElementById("feature-info");
          feature_div.innerHTML = "";
          for (var key in feature.attributes ) {
            feature_div.innerHTML +=
              key + ": " + feature.attributes[key] + "<br>";
            }
        },
      // onUnselect: function(feature){
      //   document.getElementById("feature-info").innerHTML = "hover over a feature";
      // }
  });
  map.addControl(select_ctrl);
  select_ctrl.activate();

}

function _lon2merc(lon) {
  return 20037508.34 * lon / 180;
}

function _lat2merc(lat) {
  var PI = 3.14159265358979323846;
  lat = Math.log(Math.tan( (90 + lat) * PI / 360)) / (PI / 180);
  return 20037508.34 * lat / 180;
}
  
  
//Legend

//Menu Toggle

