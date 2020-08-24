FROM python:3-alpine3.11

LABEL maintainer="bing@illinois.edu"

RUN mkdir -p /app/eventservice/events-images/

WORKDIR /app
COPY eventservice/events.yaml /app/
COPY eventservice /app/eventservice/
COPY lib /lib/


RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip build-base && \
  pip install --upgrade pip && \
  pip install -r /app/eventservice/requirements.txt --no-cache-dir && \
  apk del build-dependencies


VOLUME /var/cache/app
WORKDIR /app/eventservice/api

CMD ["gunicorn", "events_rest_service:app", "--config", "/app/eventservice/api/gunicorn.config.py"]
