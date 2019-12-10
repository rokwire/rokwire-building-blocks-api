FROM python:3-stretch

LABEL maintainer="sandeeps@illinois.edu"

WORKDIR /app

COPY appconfigservice/api .
COPY appconfigservice/requirements.txt requirements.txt
COPY appconfigservice/gunicorn.config.py gunicorn.config.py
COPY lib ../lib/

ENV APP_CONFIG_MONGO_URL=""

RUN pip install -r ./requirements.txt
WORKDIR /app/appconfigservice/api
RUN mv /lib .

# For using DocumentDB
#RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

#VOLUME /var/cache/app

#CMD ["gunicorn", "appconfig_rest_service:app", "--config", "./gunicorn.config.py"]
#gunicorn appconfig_rest_service:app --config ./gunicorn.config.py