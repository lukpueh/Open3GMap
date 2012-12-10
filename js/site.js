$(document).ready(function(){

  //outsource to configfile
  var network_dict = {
    "GPRS" : "#FF0000",
    "EDGE" : "#FF7F00",
    "UMTS" : "#FFFF00",
    "HSPA" : "#7FFF00",
    "HSUPA" : "#00FF00",
    "HSDPA" : "#00FF7F",
    "HSPAP" : "#00FFFF"
  };



  var legend = document.getElementById('color-info');
  for (var key in network_dict) {
    var canvas_container = document.createElement('div');
    canvas_container.setAttribute('class', 'canvas_container');
    legend.appendChild(canvas_container);
    
    
    var canvas = document.createElement('canvas');
    canvas_container.appendChild(canvas);
    
    canvas.setAttribute('id', key + '_canvas');
    canvas.setAttribute('width', "30px");
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
  
});
