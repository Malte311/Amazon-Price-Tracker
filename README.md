# Amazon-Price-Tracker

A simple tool to track prices on amazon.de.
> Note: Other amazon sites, such as amazon.com, wont work. If you want to track prices on other
> amazon websites different from amazon.de, you have to adjust the `/py-code/scraper.py` file. In the
> `check_price()` function, exchange the id for the title element as well as the class for the
> price element with the correct value for that other website. Moreover, the hardcoded strings inside
> the if statements as well as the currency sign have to be adjusted, too.
>
> Also remember that you should not make this service publicly available on your server because users
> can type in arbitrary inputs which are not checked properly (which can be very dangerous).

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

A cronjob every 30 minutes could look like this:

```bash

*/30 * * * * /bin/sh /var/docker-compose/amazon-scraper/cron.sh

```

Note that the scraper has a session limit of 5 connections per session in order to avoid
too many requests at the same time. This limit can be changed by adjusting the parameter
given to `scraper.py` in the file `cron.sh`.