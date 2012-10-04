var map;
var layer_mapnik;
var operator_layer;
var operators = new Array('generic', 'one','telering','max');
//var networks = new Array("HSPAP","HSDPA","HSUPA","UMTS"); // used only for testdatageneration
var network_dict = {
  "GPRS" : "#FF0000",
  "EDGE" : "#FF7F00",
  "UMTS" : "#FFFF00",
  "HSPA" : "#7FFF00",
  "HSUPA" : "#00FF00",
  "HSDPA" : "#00FF7F",
  "HSPAP" : "#00FFFF"
};

var point_style_dict = {
  "point_radius" : 6,
  "fill_opacity" : 1,
  "stroke_opacity" : 1,
  "stroke_width" : 0.1
};

var selectControl, selectedFeature; //pop up
function draw_map() {

  //Default position and zoom Level for the map.

  var map_lon = 16.355;
  var map_lat = 48.22;
  var map_zoom = 16;
  
  map = new OpenLayers.Map('map');
  layer_mapnik = new OpenLayers.Layer.OSM("Mapnik");
  map.addLayer(layer_mapnik);
  map.setCenter(new OpenLayers.LonLat(lon2merc(map_lon), lat2merc(map_lat)), map_zoom);

  
  //Style partially static, partially dependant on Feature (point)
  var style = new OpenLayers.Style({
      pointRadius: "${point_radius}",
      fillColor: "${fill_color}",      
      strokeWidth: "${stroke_width}",
      fillOpacity: point_style_dict.fill_opacity,
      strokeOpacity: point_style_dict.stroke_opacity,
    });
  var style_map = new OpenLayers.StyleMap(style);

  // One Layer for each operator 
  operator_layer = new Array();
  for (i = 0; i < operators.length; i++) {
    operator_layer[i] = new OpenLayers.Layer.Vector(operators[i], {styleMap: style_map});
    map.addLayer(operator_layer[i]);
  }
  map.addControl(new OpenLayers.Control.LayerSwitcher());

  
  //Handler for PopUp
  selectControl = new OpenLayers.Control.SelectFeature(operator_layer, {
                hover: true,
                onSelect: onFeatureSelect,
                onUnselect: onFeatureUnselect
                });
  map.addControl(selectControl);
  selectControl.activate();
                
  //map.events.register('click', map, map_click);   
  
  // CSV import
  if (window.XMLHttpRequest) { 
    xmlhttp = new XMLHttpRequest();
  } else {
    xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
  }
  xmlhttp.open('POST','o3gm_readings_201210021639.txt',false);
  xmlhttp.send('');
  
  var csv_lines = new Array()
  csv_lines = xmlhttp.responseText.split(/\n/g);
  // ###########
  // Read CSV lines
  // if any changes to csv layout are made, this should be considered here
  //runtime timestamp mcc mnc cell_id nw_type rssi loc_source lat lon alt accuracy battery_level tac vendor model
  var definition = csv_lines[0].split(' ');

  for (i=1; i < csv_lines.length; i++) {
    
    try {
      var csv_values = csv_lines[i].split(' ');
      var dict = {};

      for (l=0; l < definition.length; l++) {
        dict[definition[l]] = csv_values[l];
      }
      
      // Dictionary of Data that is shown in the PopUp Window
      var popup_data_dict = {
        //"operator" : dict['mcc'],
        "network" : dict['nw_type'],
        //"signal strength" : dict['tac']
      };
    
      // Create a new feature (visualized point)
      var feature = new OpenLayers.Feature.Vector(
        new OpenLayers.Geometry.Point(
          lon2merc(parseFloat(dict['lon'])), lat2merc(parseFloat(dict['lat']))), {
          point_radius: point_style_dict.point_radius,
          stroke_width: point_style_dict.stroke_width,
          fill_color: network_dict[dict['nw_type']],
          popup_data_dict: popup_data_dict
        });
    
      //append features to according operator layer
     // for (k=0; k < operator_layer.length; k++){
        //if (operator_layer[k].name == dict['operator'] )  {
          operator_layer[0].addFeatures(feature);  
       // }
      //}
    } catch(err){
      //alert(err);
    }
  } // END For CSV lines
}

function onPopupClose(evt) {
  selectControl.unselect(selectedFeature);
}

function onFeatureSelect(feature) {
  selectedFeature = feature;
  popup = new OpenLayers.Popup.AnchoredBubble("info");
  popup.lonlat = feature.geometry.getBounds().getCenterLonLat();
  popup.opacity = 0.9;
  popup.contentSize = new OpenLayers.Size(150,80);
  
  popup.contentHTML = "";
  for (var key in feature.data.popup_data_dict ) {
    popup.contentHTML += "<br>" + key + ": " + feature.data.popup_data_dict[key];
  }
  
  feature.popup = popup;
  map.addPopup(popup);
}

function onFeatureUnselect(feature) {
  map.removePopup(feature.popup);
  feature.popup.destroy();
  feature.popup = null;
}    
  
function lon2merc(lon) {
  return 20037508.34 * lon / 180;
}

function lat2merc(lat) {
  var PI = 3.14159265358979323846;
  lat = Math.log(Math.tan( (90 + lat) * PI / 360)) / (PI / 180);
  return 20037508.34 * lat / 180;
}
