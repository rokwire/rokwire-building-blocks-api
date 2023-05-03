FROM python:3.9-alpine

LABEL maintainers="sandeeps@illinois.edu,"
LABEL authors="ywkim@illinois.edu,"

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/loggingservice

COPY loggingservice .

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/loggingservice/api

COPY loggingservice/logging.yaml .

#ENV LOGGING_MONGO_URL=""
ENV LOGGING_URL_PREFIX=""

CMD ["gunicorn", "logging_rest_service:app", "--config", "/usr/src/app/loggingservice/api/gunicorn.config.py"]