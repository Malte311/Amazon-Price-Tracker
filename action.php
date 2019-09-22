<?php
error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

$input_url = $_POST["input-url"];

$file_path = 'urls.json';

if (!file_exists($file_path)) {
	$file = fopen($file_path, 'w');
	fclose($file);
}

$data = json_decode(file_get_contents($file_path), true);

$data['urls'][] = $input_url;

file_put_contents($file_path, json_encode($data, JSON_PRETTY_PRINT));

?>