var point_style_map = new OpenLayers.StyleMap({
   "default": new OpenLayers.Style({
          pointRadius: 3,
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
              return network_dict[feature.attributes.prevailing_nw_type];
            }
          }
        }),
  "select": new OpenLayers.Style({
        fillOpacity: 1,
        strokeWidth: 1,
    })
  });
  
var grid_style_map = new OpenLayers.StyleMap({
 "default": new OpenLayers.Style({
        fillColor: "#FF7274",
        fillOpacity: 0.4,
      })
  });