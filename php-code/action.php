<?php
error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

$input_thresh = floatval(str_replace(',', '.', $_POST["input-thresh"]));
$input_url = $_POST["input-url"];

if (empty($input_thresh)) {
	$input_thresh = 0;
}

$file_path = __DIR__ . '/data/urls.json';

if (!file_exists($file_path)) {
	$file = fopen($file_path, 'w');
	fclose($file);
	$data = array();
}
else {
	$data = json_decode(file_get_contents($file_path), true);
}

$data['urls'][] = array('url' => $input_url, 'thresh' => $input_thresh);

file_put_contents($file_path, json_encode($data, JSON_PRETTY_PRINT));

?>