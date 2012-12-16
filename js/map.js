// create map
// 
// create select control
// 
// create stylemap with context
// 
// open geojson
// 
// append to a layer

var network_dict = {
    "GPRS" : "#FF0000",
    "EDGE" : "#FF7F00",
    "UMTS" : "#FFFF00",
    "HSPA" : "#7FFF00",
    "HSUPA" : "#00FF00",
    "HSDPA" : "#00FF7F",
    "HSPAP" : "#00FFFF"
  };


$(document).ready(function(){
  
  //#### MAP
  var map_lon = 16.355, map_lat = 48.22, map_zoom = 12;
  var proj = new OpenLayers.Projection("EPSG:4326");
  var point = new OpenLayers.LonLat(map_lon, map_lat);
  var map = new OpenLayers.Map('map');
  
  var layer_mapnik = new OpenLayers.Layer.OSM( "OpenLayers Mapnik");
  map.addLayer(layer_mapnik);

  map.setCenter(point.transform(proj, map.getProjectionObject()), map_zoom);
  map.addControl(new OpenLayers.Control.KeyboardDefaults());
    map.addControl(new OpenLayers.Control.LayerSwitcher());

  
  //#### STYLE
  
   var point_style = new OpenLayers.Style({
            pointRadius: 5,
            fillColor: "${fill}",
            fillOpacity: 0.7,
            strokeWidth: 0
          }, {
            context: {
              fill: function(feature) {
                return network_dict[feature.attributes.nw_type];
              }
          }
      });
      
  var point_style_map = new OpenLayers.StyleMap({"default": point_style});
  
  //#### Cluster
  // var cluster_strategy = new OpenLayers.Strategy.Cluster({distance: 4});


  //#### VECTORS 
  var geojson_format = new OpenLayers.Format.GeoJSON();
  
  var points_layer = new OpenLayers.Layer.Vector("Points",{
    styleMap: point_style_map
  }); 
  
  var cells_layer = new OpenLayers.Layer.Vector("Cells");
  var lacs_layer = new OpenLayers.Layer.Vector("Lacs");

  var layers = [points_layer, cells_layer, lacs_layer];
  map.addLayers(layers);
  
  var file_name = "data/points.json";
  $.get(file_name, function(data,status) {
    points_layer.addFeatures(geojson_format.read(data));
  });
  file_name = "data/cells.json";
  $.get(file_name, function(data,status) {
    cells_layer.addFeatures(geojson_format.read(data));
  });
  
  file_name = "data/lac.json";
  $.get(file_name, function(data,status) {
    lacs_layer.addFeatures(geojson_format.read(data));
  });
  


  //### SELECT
  var options = {
    hover: true,
    onSelect: function(feature){
      $("#feature-info").html("");
      for (var key in feature.attributes) {
        $("#feature-info").append(key + ": " + feature.attributes[key] +"<br>");
      };
    }
  };
  var select = new OpenLayers.Control.SelectFeature(layers, options);
  map.addControl(select);
  select.activate();
  
  
});