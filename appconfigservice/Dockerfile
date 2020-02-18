FROM python:3-stretch

LABEL maintainer="sandeeps@illinois.edu"

WORKDIR /app

COPY appconfigservice ./appconfigservice
COPY lib ../lib/
COPY rokwire.yaml .

ENV APP_CONFIG_MONGO_URL=""
ENV APP_CONFIG_URL_PREFIX=""

RUN pip install -r ./appconfigservice/requirements.txt
WORKDIR /app/appconfigservice/api

VOLUME /var/cache/app

CMD ["gunicorn", "appconfig_rest_service:app", "--config", "../gunicorn.config.py"]