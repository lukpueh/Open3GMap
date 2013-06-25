var points_layer, cells_layer, grid_layer;

$(document).ready(function(){
  
  site();
  
  // //#### MAP
  var map_lon = 16.355, map_lat = 48.22, map_zoom = 12;
  var map = new OpenLayers.Map('map');
  var layer_mapnik = new OpenLayers.Layer.OSM("OpenLayers Mapnik");
  map.addLayer(layer_mapnik);
  
  function setCenter() {
    var proj = new OpenLayers.Projection("EPSG:4326");
    var point = new OpenLayers.LonLat(map_lon, map_lat);
    map.setCenter(point.transform(proj, map.getProjectionObject()), map_zoom);
  }  
  setCenter();
  
  map.addControl(new OpenLayers.Control.KeyboardDefaults());
  
  grid_layer = new OpenLayers.Layer.Vector("Grid", {
     styleMap: grid_style_map,
      strategies: [new OpenLayers.Strategy.BBOX({ratio: 1})],
      protocol: new OpenLayers.Protocol.HTTP({
         // url: "https://skylla.fc.univie.ac.at/openlayers/o3gm/cell_json/",
         url: "http://127.0.0.1:8000/o3gm/point_json/",
         format: new OpenLayers.Format.GeoJSON(),
      })
   });
  
  // //The Point Layer is only shown, above zoom level .. (for performance)
  // points_layer = new OpenLayers.Layer.Vector("Points", {
  //    styleMap: point_style_map,
  //     strategies: [new OpenLayers.Strategy.BBOX({ratio: 1})],
  //     protocol: new OpenLayers.Protocol.HTTP({
  //        // url: "https://skylla.fc.univie.ac.at/openlayers/o3gm/cell_json/",
  //        url: "http://127.0.0.1:8000/o3gm/point_json/",
  //        format: new OpenLayers.Format.GeoJSON(),
  //     })
  //  });

  cells_layer = new OpenLayers.Layer.Vector("Cells", {
     styleMap: polygon_style_map,
     strategies: [new OpenLayers.Strategy.Fixed()],
     protocol: new OpenLayers.Protocol.HTTP({
        // url: "https://skylla.fc.univie.ac.at/openlayers/o3gm/cell_json/",
        url: "http://127.0.0.1:8000/o3gm/cell_json/",
        format: new OpenLayers.Format.GeoJSON()
     })
  });
  // 
  // var lacs_layer = new OpenLayers.Layer.Vector("Lacs", {
  //    styleMap: polygon_style_map,
  //    strategies: [new OpenLayers.Strategy.Fixed()],
  //    protocol: new OpenLayers.Protocol.HTTP({
  //       // url: "https://skylla.fc.univie.ac.at/openlayers/o3gm/lac_json/",
  //       url: "http://127.0.0.1:8000/o3gm/lac_json/",
  //       format: new OpenLayers.Format.GeoJSON()
  //    })
  // });

  var layers = [grid_layer];
  //var layers = [points_layer, cells_layer, lacs_layer];

  map.addLayers(layers);
  
  
  //## Register Select
  var select = new OpenLayers.Control.SelectFeature(layers, select_options);
  map.addControl(select);
  select.activate();

  //### HOMEBUTTON
  // $('#controls').append("<div id='get-home' class='click click-button'>to Vienna!</div>");
  // $('#get-home').click(setCenter);
  // 
  // $('#downloads').append("<a href='https://skylla.fc.univie.ac.at/openlayers/o3gm/point_json_file/' target='_blank'>"
  //                       +"<div class='click click-button'>download points</div></a>");
  // 
  // $('#downloads').append("<a href='https://skylla.fc.univie.ac.at/openlayers/o3gm/cell_json_file/' target='_blank'>"
  //                       +"<div class='click click-button'>download cells</div>");
  // 
  // $('#downloads').append("<a href='https://skylla.fc.univie.ac.at/openlayers/o3gm/lac_json_file/' target='_blank'>"
  //                       +"<div class='click click-button'>download lacs</div>");

                
                
  //#### Controls
  // $(document).on('change', '.show_layer', function(e) {
  //   var layer = eval(e.target.value);
  //   layer.getVisibility() ? layer.setVisibility(0) : layer.setVisibility(1);
  // });
  
  // $('#controls').append("<table class='sidebar-table'>" + 
  //                       "<tr><td> Points </td>" + 
  //                       "<td><input type='checkbox' class='show_layer' checked='checked'  value='points_layer'></td></tr>" + 
  //                       "<tr><td> Cells </td>" + 
  //                       "<td><input type='checkbox' class='show_layer' checked='checked' value='cells_layer'></td></tr>" + 
  //                       "<tr><td> Lacs </td>" + 
  //                       "<td><input type='checkbox' class='show_layer' checked='checked' value='lacs_layer'></td></tr>" + 
  //                       "</table>");


   
  // $('select').change(function() {
  //       OpenLayers.Request.GET({
  //       url: "http://127.0.0.1:8000/o3gm/point_json/",
  //       params: {
  //         nw_type : $('[name=select-nw-type]').val(),
  //         operator : $('[name=select-operator]').val()
  //       },
  //       success: function(request) {
  //  
  // 
  //         points_layer.destroyFeatures(); 
  //         points_layer.addFeatures(new OpenLayers.Format.GeoJSON().read(request.responseText)); 
  //         console.log(points_layer);
  //         points_layer.redraw();
  //       }
  //   });
  // 
  // 
  // });


});