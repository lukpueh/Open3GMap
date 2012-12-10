<?php

function _is_left($a, $b, $c){
  //area of a triangle
  // is area is negative, poin is on the left
  $area = $a["lon"]*($b["lat"]-$c["lat"]) + $b["lon"]*($c["lat"]-$a["lat"]) + $c["lon"]*($a["lat"]-$b["lat"]);
  return ($area < 0 ) ? true : false;
}

function jarvis($all_points){
  
  # Find leftmost point in S
  $current_point = $all_points[0];
  foreach($all_points as $point) {
    if ($point["lon"] < $current_point["lon"])
      $current_point = $point;
  }
  
  $hull_points = array();
  $k = 0;
  do  {
    $hull_points[] = $current_point;    
    $end_point = $all_points[0];
    
    foreach($all_points as $point){
      if (($end_point == $current_point) 
        or _is_left($current_point, $point, $end_point)) {
        $end_point = $point;
      }
        
    }
     $k++;
    $current_point = $end_point;
  } while ($end_point != $hull_points[0]);
  return $hull_points;
}
?>




