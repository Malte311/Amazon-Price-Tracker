# Amazon-Price-Tracker

A simple tool to track prices on amazon.de.
> Note: Other amazon sites, such as amazon.com, wont work. If you want to track prices on other
> amazon websites other than amazon.de, you have to adjust the `/py-code/scraper.py` file. In the
> `check_price()` function, exchange the id for the title element as well as the class for the
> price element with the correct value for that other website.

## Installation (via Docker)

1. Download this repository:

```bash

git clone git@github.com:Malte311/Amazon-Price-Tracker.git

```

2. Adjust the `docker-compose.yml` file. Specify the correct server url and port. If you want
to get notifications via email, you need a gmail account. Set the `MAIL_USER` variable to the
sender email (has to be a gmail account) and `MAIL_PW` to the corresponding app password (not
the "normal" password!). The receiving email address can use any email provider.

```yaml

version: "2"

services:
  web:
    image: malte311/amazon-price-tracker:latest
    container_name: amazon-scraper
    ports:
      - "127.0.0.1:8080:80"
    volumes:
      - ./data/:/php-code/data/
    restart: always
    environment:
      - SERVERURL=https://example.com/amazon-scraper
      - MAIL_USER=example@gmail.com
      - MAIL_PW=password
      - MAIL_RECEIVER=example@mail.com

```

3. Get the newest Docker image and start a Docker container (inside of the project folder):

```bash

docker-compose pull
docker-compose up -d

```

4. Install a cronjob to run the scraper periodically.

```bash

chmod +x cron.sh
crontab -e -u root

```

A daily cronjob at 06:00 am could look like this:

```bash

00 6 * * * /bin/sh /var/docker-compose/amazon-scraper/cron.sh

```