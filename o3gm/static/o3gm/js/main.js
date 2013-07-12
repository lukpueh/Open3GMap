var points_layer, cells_layer, lacs_layer, grid_layer;
var espg_4326 = new OpenLayers.Projection("EPSG:4326");
var espg_900913 = new OpenLayers.Projection("EPSG:900913");

$(document).ready(function(){
  
  site();
  
  // //#### MAP
  var map_lon = 16.355, map_lat = 48.22, map_zoom = 12;
  var map = new OpenLayers.Map('map');
  var layer_mapnik = new OpenLayers.Layer.OSM("OpenLayers Mapnik");
  map.addLayer(layer_mapnik);
  
  function setCenter() {
    var point = new OpenLayers.LonLat(map_lon, map_lat);
    map.setCenter(point.transform(espg_4326, map.getProjectionObject()), map_zoom);
  }  
  setCenter();
  
  map.addControl(new OpenLayers.Control.KeyboardDefaults());

  
  //The Point Layer is only shown, above zoom level .. (for performance)
  points_layer = new OpenLayers.Layer.Vector("Points", {
     styleMap: point_style_map,
   });

  // cells_layer = new OpenLayers.Layer.Vector("Cells", {
  //    styleMap: polygon_style_map,
  //    strategies: [new OpenLayers.Strategy.Fixed()],
  //    protocol: new OpenLayers.Protocol.HTTP({
  //       url: "/o3gm/cell_json/",
  //       format: new OpenLayers.Format.GeoJSON()
  //    })
  // });
  // 
  // lacs_layer = new OpenLayers.Layer.Vector("Lacs", {
  //    styleMap: polygon_style_map,
  //    strategies: [new OpenLayers.Strategy.Fixed()],
  //    protocol: new OpenLayers.Protocol.HTTP({
  //       url: "/o3gm/lac_json/",
  //       format: new OpenLayers.Format.GeoJSON()
  //    })
  // });
  
   
  // grid_layer = new OpenLayers.Layer.Vector("Grid", {
  //    styleMap: grid_style_map,
  //     strategies: [new OpenLayers.Strategy.BBOX({ratio: 1})],
  //     protocol: new OpenLayers.Protocol.HTTP({
  //        url: "/o3gm/point_json/",
  //        format: new OpenLayers.Format.GeoJSON(),
  //     })
  //  });

  var layers = [points_layer];
  //var layers = [points_layer, cells_layer, lacs_layer, grid_layer];

  map.addLayers(layers);
  
  
  //## Register Select
  var select = new OpenLayers.Control.SelectFeature(layers, select_options);
  map.addControl(select);
  select.activate();

  //### HOMEBUTTON
  $('#links').append("<div id='get-home' class='click click-button'>to Vienna!</div>");
  $('#get-home').click(setCenter);
  
  //### DOWNLOAD
  $('#links').append("<a href='/o3gm/point_json_file/' target='_blank'>"
                        +"<div class='click click-button'>download points</div></a>");
  
  $('#links').append("<a href='/o3gm/cell_json_file/' target='_blank'>"
                        +"<div class='click click-button'>download cells</div></a>");
  
  $('#links').append("<a href='/o3gm/lac_json_file/' target='_blank'>"
                        +"<div class='click click-button'>download lacs</div></a>");
                      
                
  //#### Controls
  // $(document).on('change', '.show_layer', function(e) {
  //   var layer = eval(e.target.value);
  //   layer.getVisibility() ? layer.setVisibility(0) : layer.setVisibility(1);
  // });
  // 
  // $('#controls').append("<table class='sidebar-table'>" + 
  //                       "<tr><td> Points </td>" + 
  //                       "<td><input type='checkbox' class='show_layer' checked='checked'  value='points_layer'></td></tr>" + 
  //                       "<tr><td> Cells </td>" + 
  //                       "<td><input type='checkbox' class='show_layer' checked='checked' value='cells_layer'></td></tr>" + 
  //                       "<tr><td> Lacs </td>" + 
  //                       "<td><input type='checkbox' class='show_layer' checked='checked' value='lacs_layer'></td></tr>" + 
  //                       "</table>");

    //### DATA OPTIONS
  
    $('[name=select-data]').change(function(evt) {
        var src = $(this).val();
        $.get('/o3gm/data_options/', {data_src: src}, function(data){
          $('#dataOptions').html(data);
          });
        
    });
   
  $('#submit').click(function() {
        $("#submit").attr("disabled", "disabled");
        var bounds = map.getExtent();
        bounds = bounds.transform(espg_900913, espg_4326).toBBOX();
        
          OpenLayers.Request.GET({
              url: "/o3gm/point_json/",
              params: {
              bbox            : bounds,
              data_source     : $('[name=select-data]').val(),
              nw_type         : $('[name=select-nw-type]').val(),
              operator        : $('[name=select-operator]').val()
             },
          success: function(request) {
             
            points_layer.destroyFeatures(); 
            var format = new OpenLayers.Format.GeoJSON();
            format.externalProjection = espg_4326;
            format.internalProjection = espg_900913;
            var features = format.read(request.responseText);
            points_layer.addFeatures( features ); 
            points_layer.redraw();
            $("#feedback").html("retrieved points: " + features.length);
            $("#submit").removeAttr("disabled");
          }
      });
    
    
    });


});