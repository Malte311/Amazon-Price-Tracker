#!/bin/sh
php -r 'file_put_contents( "/py-code/config.json", json_encode( array( "mail-user" => $_ENV["MAIL_USER"], "mail-pw" => $_ENV["MAIL_PW"], "mail-receiver" => $_ENV["MAIL_RECEIVER"] ) ) );'
php -r 'if (!is_file("/php-code/data/urls.json")) { file_put_contents( "/php-code/data/urls.json", json_encode( array( "urls" => [] ) ) ); }'

cd /py-code/ && python3 ./update_user_agents.py

chown www-data:www-data /py-code/config.json
chown -R www-data:www-data /php-code/data/
