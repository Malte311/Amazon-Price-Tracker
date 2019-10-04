<?php
error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

define('KIMB-Classes', 'ok');
require_once(__DIR__ . '/classes/autoload.php');

$data_path = __DIR__ . '/data/';
init();

function init() {
	global $data_path;

	Template::setServerURL(!empty($_ENV['SERVERURL']) ? $_ENV['SERVERURL'] : 'http://localhost:8000');

	$main_template = new Template('main');
	$charts_template = new Template('charts');

	$all_charts = create_charts(scandir($data_path));

	$charts_template->setMultipleContent('Chart', $all_charts);
	$main_template->includeTemplate($charts_template);
	
	if (isset($_GET['uri']) && ($_GET['uri'] === 'err404' || $_GET['uri'] === 'err403')) {
		display_alert($main_template, 'Error' . ($_GET['uri'] == 'err404' ? '404' : '403'), 'danger');
	}
	else if (isset($_GET['saved'])) {
		display_alert($main_template, 'Saved successfully!', 'success');
	}
	
	$main_template->output();
}

function create_charts($files) {
	global $data_path;
	
	$all_charts = array();
	foreach ($files as $file) {
		if (is_json_data_file($file)) {
			$data_set = json_decode(file_get_contents($data_path . $file), true);
	
			$prices = [];
			foreach ($data_set as $day) {
				if (is_array($day)) {
					$prices[] = $day['price'];
				}
			}
			
			$labels = array_diff(array_keys($data_set), ['title', 'url']);
			$title = strlen($data_set['title']) > 65 ?
					substr($data_set['title'], 0, 65) . '...' : $data_set['title'];
			$all_charts[] = array(
				"FILE" => $file,
				"LABELTEXT" => json_encode($labels),
				"DATATEXT" => json_encode($prices),
				"TITLE" => $title
			);
		}
	}

	return $all_charts;
}

function is_json_data_file($file) {
	$file_extension = '.json';
	$offset = strlen($file) - strlen($file_extension);
	return substr_compare($file, $file_extension, $offset, strlen($file_extension)) === 0
			&& $file != 'urls.json';
}

function display_alert($template, $msg, $color) {
	$template->setContent('NOTECOLOR', $color);
	$template->setContent('NOTE', $msg);
	$template->setContent('NOTEDISPLAY', 'block');
}
?>