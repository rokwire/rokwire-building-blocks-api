FROM python:3-stretch

LABEL maintainer="sandeeps@illinois.edu"

WORKDIR /app

COPY appconfigservice ./appconfigservice
COPY lib ../lib/
COPY rokwire.yaml .

ENV APP_CONFIG_MONGO_URL=""

RUN pip install -r ./requirements.txt
WORKDIR /app/appconfigservice/api

VOLUME /var/cache/app

CMD ["gunicorn", "appconfig_rest_service:app", "--config", "../gunicorn.config.py"]