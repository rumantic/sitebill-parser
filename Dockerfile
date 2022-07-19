#FROM sitebill/python-crawler-env
FROM sitebill/python-crawler-env
MAINTAINER kondin@etown.ru

#ENV MONGO_HOST="192.168.1.37"
#ENV MONGO_PORT="27017"
#ENV MONGO_USER=""
#ENV MONGO_PASS=""

RUN apt-get -y install mc
RUN apt-get -y install git


COPY . .

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
#RUN touch /etc/environment

#RUN crontab crontab
RUN crontab -l | { cat; echo "* * * * * /usr/local/bin/python3.7 /crawler.py  >> /var/log/cron.log 2>&1"; } | crontab -

#CMD ["echo", "START"]
#CMD ["echo", "$MONGO_HOST"]

#CMD ["env", ">> /etc/environment"]
#CMD ["echo", "$MONGO_HOST", ">>", "/etc/environment"]
#CMD ["sh", "-c", "echo \"TEST MESSAGE\""]
#CMD ["sh", "-l", "-c", "env >> /etc/environment"]
#CMD ["sh", "-c", "echo \"MONGO_HOST=$MONGO_HOST\" >> /etc/environment"]
#CMD ["sh", "-c", "echo \"MONGO_PORT=$MONGO_PORT\" >> /etc/environment"]
#CMD ["sh", "-c", "echo \"MONGO_USER=$MONGO_USER\" >> /etc/environment"]
#CMD ["sh", "-c", "echo \"MONGO_PASS=$MONGO_PASS\" >> /etc/environment"]

# First run on startup
#CMD ["sh", "-c", "env >> /etc/environment"]
#CMD ["sh", "-c", "/usr/local/bin/python3.7 /crawler.py >> /var/log/cron.log 2>&1"]
#CMD ["/usr/local/bin/python3.7", "/crawler.py", ">>", "/var/log/cron.log", "2>&1"]
#CMD ["sh", "-c", "echo \"TEST\" >> /etc/environment"]

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

