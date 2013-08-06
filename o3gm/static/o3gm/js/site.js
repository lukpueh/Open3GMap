

function site(){
  
  //navigation
  $('.nav-item').click(function(evt){
    $('.nav-target').hide();
    $('.nav-item').removeClass("active");
    
    $('#' + evt.target.id).addClass("active");
    $('#' + evt.target.getAttribute("data-target")).show();
  });
  
  
  //Sidebar Toggle
  $('#sidebar-tg').toggle(
    function() {
      $('#map').animate({left: 12});
      $('#sidebar-tg').animate({left: 1});
      $('#sidebar').hide();
    }, function() {
      $('#map').animate({ left: 233 });
      $('#sidebar-tg').animate({ left: 222 });
      $('#sidebar').show();
    });
   
  //legend
  var legend = document.getElementById('color-info');
  for (var key in network_dict) {
    var canvas_container = document.createElement('span');
    canvas_container.setAttribute('class', 'canvas-container');
    legend.appendChild(canvas_container);
    
    
    var canvas = document.createElement('canvas');
    canvas_container.appendChild(canvas);
    
    canvas.setAttribute('id', key + '-canvas');
    canvas.setAttribute('width', "22px");
    canvas.setAttribute('height', "20px");
    var context = canvas.getContext('2d');
    context.beginPath();
    context.arc(10, 12, 8, 0, 2 * Math.PI, false);
    context.fillStyle = network_dict[key];
    context.fill();
    
    var tag = document.createElement('label');
    tag.setAttribute('for', key + '-canvas');
    tag.setAttribute('class', "canvas-label");
    tag.innerHTML = key;
    canvas_container.appendChild(tag);
  }
}



  