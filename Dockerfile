FROM sitebill/python-crawler-env
MAINTAINER kondin@etown.ru

RUN mkdir app
RUN apt-get -y install mc
RUN apt-get -y install git

COPY . /app

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#RUN crontab crontab
RUN crontab -l | { cat; echo "* * * * * /usr/local/bin/python3.7 /app/crawler.py  >> /var/log/cron.log 2>&1"; } | crontab -

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

