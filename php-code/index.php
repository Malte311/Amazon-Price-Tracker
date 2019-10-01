<?php
error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

define('KIMB-Classes', 'ok');
require_once(__DIR__ . '/classes/autoload.php');

Template::setServerURL(!empty($_ENV['SERVERURL']) ? $_ENV['SERVERURL'] : 'http://localhost:8000');

$all_charts = array();

$file_extension = '.json';
foreach (scandir(__DIR__ . '/data/') as $file) {
	if (substr_compare($file, $file_extension, strlen($file) - strlen($file_extension), strlen($file_extension)) === 0 && $file != 'urls.json') {
		$dataSet = json_decode(file_get_contents(__DIR__ . '/data/' . $file), true);

		$prices = [];
		foreach ($dataSet as $day) {
			if (is_array($day)) {
				$prices[] = $day['price'];
			}
		}
		
		$labels = array_diff(array_keys($dataSet), ['title', 'url']);

		$all_charts[] = array(
			"FILE" => $file,
			"LABELTEXT" => json_encode($labels),
			"DATATEXT" => json_encode($prices)
		);
	}
}

$template = new Template('main');
$chartstemplate = new Template('charts');
$chartstemplate->setMultipleContent('Chart', $all_charts);
$template->includeTemplate($chartstemplate);

if( isset($_GET['uri']) && ( $_GET['uri'] === 'err404' || $_GET['uri'] === 'err403' ) ){
	$template->setContent('NOTE', '<h1> Error' . ( $_GET['uri'] == 'err404' ? '404' : '403' ) . '</h1>' );
}

$template->output();
?>
