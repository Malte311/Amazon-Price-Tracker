<!-- <?php
	$file_extension = '.json';
	foreach (scandir('./data/') as $file) {
		if (substr_compare($file, $file_extension, strlen($file) - strlen($file_extension), strlen($file_extension)) === 0 && $file != 'urls.json') {
			$dataSet = json_decode(file_get_contents(__DIR__ . $file), true);

			$prices = [];
			foreach ($dataSet as $day) {
				if (is_array($day)) {
					$prices[] = $day['price'];
				}
			}
			
			$labels = array_keys($dataSet);
		}
	}
?> -->

<?php
error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

define('KIMB-Classes', 'ok');
require_once(__DIR__ . '/php-code/autoload.php');

Template::setServerURL('http://localhost:8080/');
$template = new Template('main');
$template->output();



?>

<!-- <!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<title>Amazon-Price-Tracker</title>
	<link rel="stylesheet" type="text/css" href="/lib/bootstrap.min.css">
</head>

<body>
	<form class="form-inline" action="action.php" method="post">
		<input class="form-control mr-sm-2" type="text" placeholder="Amazon link" name="input-url" autofocus>
		<input class="form-control mr-sm-2" type="text" placeholder="Threshold" name="input-thresh">
		<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Add</button>
	</form>
	<script src="/lib/chart.min.js"></script>
	<?php
		$file_extension = '.json';
		foreach (scandir('./data/') as $file) {
			if (substr_compare($file, $file_extension, strlen($file) - strlen($file_extension), strlen($file_extension)) === 0 && $file != 'urls.json') {
				$dataSet = json_decode(file_get_contents(__DIR__ . '/data/' . $file), true);

				$prices = [];
				foreach ($dataSet as $day) {
					if (is_array($day)) {
						$prices[] = $day['price'];
					}
				}
				
				$labels = array_keys($dataSet);

				echo "<canvas id=\"$file\" width=\"500\" height=\"300\"></canvas>";

				$labels_text = json_encode($labels);
				$prices_text = json_encode($prices);

				echo
				"<script>
					new Chart('$file', {
						type: 'line',
						data: {
							labels: $labels_text,
							datasets: [{
								backgroundColor: 'rgba(255, 99, 132, 0.5)',
								borderColor: 'rgba(255, 99, 132, 1)',
								data: $prices_text,
								label: 'Dataset',
								fill: 'rgba(255, 99, 132, 0.5)'
							}]
						}
					});
				</script>";
			}
		}
	?>
</body>

</html> -->