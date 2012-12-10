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

echo json_encode($o3gm_point_dict);

?>