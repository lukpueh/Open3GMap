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
  var map = new OpenLayers.Map('map');
  var layer_mapnik = new OpenLayers.Layer.OSM( "OpenLayers Mapnik");
  map.addLayer(layer_mapnik);
  
  function setCenter() {
    var proj = new OpenLayers.Projection("EPSG:4326");
    var point = new OpenLayers.LonLat(map_lon, map_lat);
    map.setCenter(point.transform(proj, map.getProjectionObject()), map_zoom);
  }  
  setCenter();
  map.addControl(new OpenLayers.Control.KeyboardDefaults());
  //map.addControl(new OpenLayers.Control.LayerSwitcher());

  //#### STYLE 
  var point_style_map = new OpenLayers.StyleMap({
   "default": new OpenLayers.Style({
          pointRadius: 6,
          fillColor: "${fill}",
          fillOpacity: 0.8,
          strokeWidth: 0
        }, { context: { fill: function(feature) {
                return network_dict[feature.attributes.nw_type];
              }
            }
          }),
    "select": new OpenLayers.Style({
          fillOpacity: 1,
          strokeWidth: 1,
      })
    });
    
  var polygon_style_map = new OpenLayers.StyleMap({
   "default": new OpenLayers.Style({
          fillColor: "${fill}",
          fillOpacity: 0.4,
          strokeColor: "#000000",
          strokeWidth: 0.5,
        }, { context: { fill: function(feature) {
                return network_dict[feature.attributes.pnt];
              }
            }
          }),
    "select": new OpenLayers.Style({
          fillOpacity: 1,
          strokeWidth: 1,
      })
    });
        
  //#### Cluster
  // var cluster_strategy = new OpenLayers.Strategy.Cluster({distance: 4});

  //#### VECTORS 
  var geojson_format = new OpenLayers.Format.GeoJSON();
  
  var filter = new OpenLayers.Filter.Spatial( {type: OpenLayers.Filter.Spatial.BBOX});
  
  var points_layer = new OpenLayers.Layer.Vector("Points",{
    filter: [new OpenLayers.Strategy.Filter({filter: filter})],
    styleMap: point_style_map
  }); 
  
  console.log(points_layer);
  
  var cells_layer = new OpenLayers.Layer.Vector("Cells",{
    styleMap: polygon_style_map
  });
  var lacs_layer = new OpenLayers.Layer.Vector("Lacs", {
    styleMap: polygon_style_map
  });
  points_layer.setVisibility(0);
  cells_layer.setVisibility(0);
  lacs_layer.setVisibility(0);

  var layers = [points_layer, cells_layer, lacs_layer];
  map.addLayers(layers);
  
  var file_name = "data/points.json";
  var start = new Date().getSeconds();

  $.get(file_name, function(data,status) {
    points_layer.addFeatures(geojson_format.read(data));
    for(var i=0; i < data.features.length; i++){
      var x = 0;
      if (data.features[i].lon)
        x++;
      }
    var end = new Date().getSeconds(); 
    console.log(start);
    console.log(end);
    console.log(end-start);
  });
  

  file_name = "data/cells.json";
  $.get(file_name, function(data,status) {
    cells_layer.addFeatures(geojson_format.read(data));
  });
  
  file_name = "data/lacs.json";
  $.get(file_name, function(data,status) {
    lacs_layer.addFeatures(geojson_format.read(data));
  });
  
  //### Show / Hide
  
  // for (var key in network_dict){
  //   $('#controls').append("<br><input type='checkbox' class='show_nw' checked='checked' value='"+key+"'>" + key);
  // }
  // 
  // $(document).on('change', '.show_nw', function(e) {
  //   var args = eval(e.target.value);
  //   console.log(args[0]);
  //   // var features = args[1].features;
  //   // for (var i = 0; i < features.length; i++) {
  //   //   if (this.value == features[i].attributes.pnt) {
  //   //     if (features[i].style == null)
  //   //       features[i].style = { display : 'none' };
  //   //     else
  //   //       features[i].style = null;
  //   //   }
  //   // }
  //   // cells_layer.redraw();
  // });
  // 
  $(document).on('change', '.show_layer', function(e) {
    var layer =  eval(e.target.value);
    layer.getVisibility() ? layer.setVisibility(0) : layer.setVisibility(1);
  });
  
  var sidebar_table = "<table class='sidebar-table'>";
  
  
  sidebar_table += "<tr><td></td><td>Points</td><td>Cells</td><td>Lacs</td></tr>";
  sidebar_table += "<tr>";
  sidebar_table += "<td>all</td>";
  sidebar_table += "<td><input type='checkbox' class='show_layer' value='points_layer'></td>";
  sidebar_table += "<td><input type='checkbox' class='show_layer' checked='checked' value='cells_layer'></td>";
  sidebar_table += "<td><input type='checkbox' class='show_layer' checked='checked' value='lacs_layer'></td>";
  sidebar_table += "</tr>";
      
  for(var key in network_dict) {
    sidebar_table += "<tr>";
    sidebar_table += "<td>"+ key.toLowerCase(); +"</td>";
    sidebar_table += "<td><input type='checkbox' class='show_nw' checked='checked' value='[\'"+key+"\', points_layer]'></td>";
    sidebar_table += "<td><input type='checkbox' class='show_nw' checked='checked' value='[\'"+key+"\', cells_layer]'></td>";
    sidebar_table += "<td><input type='checkbox' class='show_nw' checked='checked' value='l\'"+key+"\', lacs_layer'></td>";
    sidebar_table += "</tr>";
  }
  sidebar_table += "</table>"
  
  $('#controls').append(sidebar_table);

 
   
  
  //### HOMEBUTTON
  $('#controls').append("<div id='get-home' class='click-bar'>set center</div>");
  $('#get-home').click(setCenter);

  //### SELECT
  
  function selectPoint(attr){
    $("#feature-info").append(
      "<table class='sidebar-table'>"+
      "<tr><td> Type </td><td>"+ attr["type"] +"</td><td>"+
      "<tr><td> Cell ID</td><td>"+ attr["cell_id"] +"</td><td>"+
      "<tr><td> Lac ID </td><td>"+ attr["lac"] +"</td><td>"+
      "<tr><td> Tac ID </td><td>"+ attr["tac"] +"</td><td>"+     
      "<tr><td> Operator  </td><td>"+ attr["mcc"]+ attr["mnc"] +"</td><td>"+
      "<tr><td> IP </td><td>"+ attr["ip"] +"</td><td>"+
      "<tr><td> RSSI  </td><td>"+ attr["rssi"] +"</td><td>"+
      "<tr><td> Longitude  </td><td>"+ attr["lon"] +"</td><td>"+
      "<tr><td> Latitude  </td><td>"+ attr["lat"] +"</td><td>"+
      "<tr><td> GPS accuracy </td><td>"+ attr["accuracy"] +"</td><td>"+
      "<tr><td> Vendor </td><td>"+ attr["vendor"] +"</td><td>"+
      "<tr><td> Model </td><td>"+ attr["model"] +"</td><td>"+
      "<tr><td> Battery  </td><td>"+ attr["battery_level"] +"</td><td>"+
      "</table>"
      );
  }
  
  function _makeNwRows(attr) {
    rows = ""
    for (var key in attr) {
      rows += "<tr><td>"+key+"</td><td>"+ attr[key] +"</td><td>";
    }
    return rows
  }
  
  function selectCell(attr){
    $("#feature-info").append(
      "<table class='sidebar-table'>"+
      "<tr><td> Type </td><td>"+ attr["type"] +"</td><td>"+
      "<tr><td> Cell ID</td><td>"+ attr["cell_id"] +"</td><td>"+
      "<tr><td> Lac ID </td><td>"+ attr["lac"] +"</td><td>"+
      "<tr><td> PNT </td><td>"+ attr["pnt"] +"</td><td>"+
      _makeNwRows(attr["nw_types"]) +
      "</table>"
      );
  }
  
  function selectLac(attr){
    $("#feature-info").append(
      "<table class='sidebar-table'>"+
      "<tr><td> Type </td><td>"+ attr["type"] +"</td><td>"+
      "<tr><td> Lac ID </td><td>"+ attr["lac"] +"</td><td>"+
      "<tr><td> PNT </td><td>"+ attr["pnt"] +"</td><td>"+
      _makeNwRows(attr["nw_types"]) +
      "</table>"
      );
  }
  
  var options = {
    hover: true,
    onSelect: function(feature){
      $("#feature-info").html("");
      switch (feature.attributes.type){
        case "point":
          selectPoint(feature.attributes);
          break;
        case "cell":
          selectCell(feature.attributes);
          break;
        case "lac":
          selectLac(feature.attributes);
          break;
        default:
          break;
      }
    }
  };
  var select = new OpenLayers.Control.SelectFeature(layers, options);
  map.addControl(select);
  select.activate();
  
});