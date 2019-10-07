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
	$all_charts = sort_charts($all_charts, isset($_GET['sort']) ? $_GET['sort'] : 0);

	$charts_template->setMultipleContent('Chart', $all_charts);
	$main_template->includeTemplate($charts_template);
	
	if (isset($_GET['uri']) && ($_GET['uri'] === 'err404' || $_GET['uri'] === 'err403')) {
		display_alert($main_template, 'Error' . ($_GET['uri'] == 'err404' ? '404' : '403'), 'danger');
	} else if (isset($_GET['saved'])) {
		display_alert($main_template, 'Saved successfully!', 'success');
	} else if (isset($_GET['deleted'])) {
		display_alert($main_template, 'Deleted successfully!', 'success');
	}
	
	$main_template->output();
}

function create_charts($files) {
	global $data_path;
	
	$all_charts = array();
	foreach ($files as $file) {
		if (is_json_data_file($file)) {
			$data_set = json_decode(file_get_contents($data_path . $file), true);
	
			$prices = array();
			foreach ($data_set as $day) {
				if (is_array($day)) {
					$prices[] = $day['price'];
				}
			}

			$diff = 0;
			$prices_size = count($prices);
			if ($prices_size > 1) {
				$diff = $prices[$prices_size - 1] - $prices[$prices_size - 2];
			}
			$labels = array_diff(array_keys($data_set), ['title', 'url']);
			$title = strlen($data_set['title']) > 65 ?
					substr($data_set['title'], 0, 65) . '...' : $data_set['title'];
			$title = str_replace('"', '', str_replace('\'', '', $title));
			$all_charts[] = array(
				"FILE" => $file,
				"LABELTEXT" => json_encode($labels),
				"DATATEXT" => json_encode($prices),
				"LINK" => $data_set['url'],
				"TITLE" => $title,
				"DIFF" => $diff,
				"DIFFCOLOR" => $diff < 0 ? 'success' : ($diff > 0 ? 'danger' : 'secondary')
			);
		}
	}

	return $all_charts;
}

function sort_charts($charts, $num) {
	switch ($num) {
		case 0: // Sort by title, ascending
			array_multisort(array_column($charts, 'TITLE'), SORT_ASC, $charts);
			break;
		case 1: // Sort by title, descending
			array_multisort(array_column($charts, 'TITLE'), SORT_DESC, $charts);
			break;
		case 2: // Sort by price, ascending
			array_multisort(array_map(function($e) {
				$e = json_decode($e);
				return $e[count($e) - 1];
			}, array_column($charts, 'DATATEXT')), SORT_ASC, $charts);
			break;
		case 3: // Sort by price, descending
			array_multisort(array_map(function($e) {
				$e = json_decode($e);
				return $e[count($e) - 1];
			}, array_column($charts, 'DATATEXT')), SORT_DESC, $charts);
			break;
		case 4: // Sort by price difference (lowest first)
			array_multisort(array_column($charts, 'DIFF'), SORT_ASC, $charts);
			break;
	}

	return $charts;
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