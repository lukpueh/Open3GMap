<?php

include("jarvis.php");

//BEGIN creating POINTS
$o3gm_point_array = array();
$file_handle = fopen("data/o3gm_readings.txt", "r");
while(($data = fgetcsv($file_handle, 4000, " ")) !== FALSE) {
  $o3gm_point_array[] = $data;
}

$o3gm_point_dict = array();
$layout = $o3gm_point_array[0]; //beware of trailing or leading whitespaces
for ($i = 1; $i < sizeof($o3gm_point_array); $i++){
  try {
  $point = array();
  for ($j = 1; $j < sizeof($layout); $j++) {
    if (sizeof($o3gm_point_array[$i]) >= sizeof($layout))
      $point[$layout[$j]] = $o3gm_point_array[$i][$j];
  }
  $o3gm_point_dict[] = $point;
  } catch (Exception $e) {}
}
//END creating POINTS

//BEGIN create cell arrays

$cell_points_dict = array();
$cell_hull_dict = array();

foreach($o3gm_point_dict as $point) {
  if (!isset($cell_points_dict[$point["cell_id"]]))
    $cell_points_dict[$point["cell_id"]] = array();
  $cell_points_dict[$point["cell_id"]][] = $point;
}

foreach($cell_points_dict as $cell_points) {
  $cell_hull_dict[] = jarvis($cell_points);
}

echo json_encode($cell_hull_dict); 
?>