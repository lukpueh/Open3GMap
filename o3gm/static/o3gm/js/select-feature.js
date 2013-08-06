//### SELECT
  
function selectPoint(id){
  $.get('/o3gm/point_properties/', { point_id: id}, function(data){
    $("#feature-info").append(data);
  });
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
    //show feature sidebar item
    $('.nav-item:eq(1)').trigger("click");
    
    switch (feature.layer.name){
      case "Points":
        selectPoint(feature.attributes.id);
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
