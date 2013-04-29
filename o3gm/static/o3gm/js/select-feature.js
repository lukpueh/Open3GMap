//### SELECT
  
function selectPoint(attr){
  $("#feature-info").append(
    "<table class='sidebar-table'>"+
    "<tr><td> Cell ID</td><td>"+ attr["cell_id"] +"</td><td>"+
    "<tr><td> Lac ID </td><td>"+ attr["lac"] +"</td><td>"+
    "<tr><td> Tac ID </td><td>"+ attr["tac"] +"</td><td>"+     
    "<tr><td> Operator  </td><td>"+ attr["mcc"]+"-"+attr["mnc"] +"</td><td>"+
    "<tr><td> IP </td><td>"+ attr["ip"] +"</td><td>"+
    "<tr><td> RSSI  </td><td>"+ attr["rssi"] +"</td><td>"+
    "<tr><td> GPS accuracy </td><td>"+ attr["accuracy"] +"</td><td>"+
    "<tr><td> Vendor </td><td>"+ attr["vendor"] +"</td><td>"+
    "<tr><td> Model </td><td>"+ attr["model"] +"</td><td>"+
    "<tr><td> Battery  </td><td>"+ attr["battery_level"] +"</td><td>"+
    "</table>"
    );
}

function selectCell(attr){
  $("#feature-info").append(
    "<table class='sidebar-table'>"+
    "<tr><td> Cell ID</td><td>"+ attr["cell_id"] +"</td><td>"+
    "<tr><td> PNT </td><td>"+ attr["prevailing_nw_type"] +"</td><td>"+
    "<tr><td> PNT count </td><td>"+ attr["prevailing_nw_count"] +"</td><td>"+
    "</table>"
    );
}

function selectLac(attr){
  $("#feature-info").append(
    "<table class='sidebar-table'>"+
    "<tr><td> Lac ID </td><td>"+ attr["lac"] +"</td><td>"+
    "<tr><td> PNT </td><td>"+ attr["prevailing_nw_type"] +"</td><td>"+
    "<tr><td> PNT count </td><td>"+ attr["prevailing_nw_count"] +"</td><td>"+
    "</table>"
    );
}

var select_options = {
  clickout: true,
  onSelect: function(feature){
    $("#feature-info").html("");
    switch (feature.layer.name){
      case "Points":
        selectPoint(feature.attributes);
        break;
      case "Cells":
        selectCell(feature.attributes);
        break;
      case "Lacs":
        selectLac(feature.attributes);
        break;
      default:
        break;
    }
  },
  onUnselect: function(feature){
    $("#feature-info").html("");
  }
  
};
