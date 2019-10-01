#!/bin/sh
php -r 'file_put_contents( "/py-code/config.json", json_encode( array( "mail-user" => $_ENV["MAIL_USER"], "mail-pw" => $_ENV["MAIL_PW"], "mail-receiver" => $_ENV["MAIL_RECEIVER"] ) ) );'
chown www-data:www-data /py-code/config.json
chown -R www-data:www-data /php-code/data/
