var map;
var layer_mapnik;
var operator_layer;
var network_layer;
//var operators = new Array('generic', 'one','telering','max');
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
  "point_radius" : 7,
  "fill_opacity" : 1,
  "stroke_opacity" : 1,
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

  //create legend
  legend();
  
  //Style partially static, partially dependant on Feature (point)
  var style = new OpenLayers.Style({
      pointRadius: "${point_radius}",
      fillColor: "${fill_color}",      
      strokeWidth: 0,
    });
  var style_map = new OpenLayers.StyleMap(style);

  network_layer = new Array();
  for (var net in network_dict) {
    var layer = new OpenLayers.Layer.Vector(net, {styleMap: style_map});
    network_layer.push(layer);
    map.addLayer(layer);
  }

  map.addControl(new OpenLayers.Control.LayerSwitcher());
  map.addControl(new OpenLayers.Control.KeyboardDefaults());

  //Handler for PopUp
  selectControl = new OpenLayers.Control.SelectFeature(network_layer, {
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
  xmlhttp.open('POST','data/o3gm_readings.txt',false);
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
        "Operator" : dict['mcc'] + "-" + dict['mnc'],
        "Network" : dict['nw_type'],
        "Signal Strength" :dict['rssi'],
        "GPS Accuracy" : dict['accuracy']
      };
    
      //alert(dict['accuracy']);
      // Create a new feature (visualized point)
      var feature = new OpenLayers.Feature.Vector(
        new OpenLayers.Geometry.Point(
          lon2merc(parseFloat(dict['lon'])), lat2merc(parseFloat(dict['lat']))), {
          point_radius: point_style_dict.point_radius,
          fill_color: network_dict[dict['nw_type']],
          popup_data_dict: popup_data_dict
        });

      //append features to according operator layer
      for (k=0; k < network_layer.length; k++){
        if (network_layer[k].name == dict['nw_type'] )  {
          network_layer[k].addFeatures(feature);  
        }
      }
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
  
  popup.contentHTML = "INFORMATION";
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


function legend(){
  var legend = document.getElementById('legend');
  for (var key in network_dict) {
    var canvas_container = document.createElement('div');
    canvas_container.setAttribute('class', 'canvas_container');
    legend.appendChild(canvas_container);
    
    
    var canvas = document.createElement('canvas');
    canvas_container.appendChild(canvas);
    
    canvas.setAttribute('id', key + '_canvas');
    canvas.setAttribute('width', "20px");
    canvas.setAttribute('height', "20px");
    var context = canvas.getContext('2d');
    context.beginPath();
    context.arc(10, 12, 8, 0, 2 * Math.PI, false);
    context.fillStyle = network_dict[key];
    context.fill();
    
    var tag = document.createElement('label');
    tag.setAttribute('for', key + '_canvas');
    tag.setAttribute('class', "canvas_label");
    tag.innerHTML = key;
    canvas_container.appendChild(tag);
    
  
  }
  
}
