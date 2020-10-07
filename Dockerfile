FROM python:3.7.5-slim-buster

# # Install and configure web scraping cron job
# RUN apt-get update && apt-get install -qq -y cron
# RUN apt-get update && apt-get install -qq -y rsyslog

# COPY crontab /etc/cron.d/scrape-mta
# RUN chmod 0644 /etc/cron.d/scrape-mta
# RUN service rsyslog start
# RUN service cron start

ENV INSTALL_PATH /mta_tracker
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "mta_tracker.app:create_app()"