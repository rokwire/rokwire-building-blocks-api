FROM python:3-alpine3.12

LABEL maintainer="minum@illinois.edu"

WORKDIR /app

COPY appconfigservice ./appconfigservice
COPY lib ../lib/
COPY appconfigservice/appconfig.yaml .
COPY appconfigservice/appconfig.yaml /app/appconfigservice/api

ENV APP_CONFIG_MONGO_URL=""
ENV APP_CONFIG_URL_PREFIX=""

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r appconfigservice/requirements.txt --no-cache-dir && \
  apk del build-dependencies
  
WORKDIR /app/appconfigservice/api

VOLUME /var/cache/app

CMD ["gunicorn", "appconfig_rest_service:app", "--config", "../gunicorn.config.py"]