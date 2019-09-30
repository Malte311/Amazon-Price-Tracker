FROM python:3
WORKDIR /py-code/
COPY --chown=www-data:www-data ./py-code/ /py-code/

FROM php:fpm-alpine

# install nginx
RUN apk add --update --no-cache nginx \
	&& mkdir -p /var/lib/nginx && chown -R www-data:www-data /var/lib/nginx \
	&& mkdir -p /var/log/nginx && chown -R www-data:www-data /var/log/nginx \
	&& mkdir -p /var/tmp/nginx && chown -R www-data:www-data /var/tmp/nginx/

# add config and php scripts
WORKDIR /php-code/
COPY --chown=www-data:www-data ./php-code/ /php-code/
COPY ./startup.sh /startup.sh

# open port
EXPOSE 80/tcp

# run nginx and php-fpm
CMD [ "sh", "/startup.sh" ]