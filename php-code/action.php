<?php
error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

if (isset($_POST['input-url']) && isset($_POST['input-thresh'])) {
	$input_url = $_POST['input-url'];
	$input_thresh = floatval(str_replace(',', '.', $_POST['input-thresh']));

	add_item($input_url, $input_thresh);
} else if (isset($_POST['file-name'])) {
	delete_item($_POST['file-name']);
}

header('Location: ' . (!empty($_ENV['SERVERURL']) ? $_ENV['SERVERURL'] : 'http://localhost:8000') . (isset($_POST['input-url']) ? '/?saved' : '/?deleted'));
http_response_code(303);

function delete_item($file_name) {
	$file_path = __DIR__ . '/data/';
	if (file_exists($file_path . $file_name)) {
		$data = json_decode(file_get_contents($file_path . $file_name), true);
		$all_urls = json_decode(file_get_contents($file_path . 'urls.json'), true);
		
		$new_urls = array();
		foreach ($all_urls['urls'] as $url) {
			if ($url['url'] !== $data['url']) {
				$new_urls[] = $url;
			}
		}

		$all_urls['urls'] = $new_urls;
		file_put_contents($file_path . 'urls.json', json_encode($all_urls, JSON_PRETTY_PRINT));
		unlink($file_path . $file_name);
	}
}

function add_item($input_url, $input_thresh) {
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
}
?>
