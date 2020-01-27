FROM python:3-alpine

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/loggingservice

COPY loggingservice .

RUN apk --update add python py-pip openssl ca-certificates py-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/loggingservice/api

COPY rokwire.yaml .

#ENV LOGGING_MONGO_URL=""
ENV LOGGING_URL_PREFIX="/logs"

CMD ["gunicorn", "logging_rest_service:app", "--config", "/usr/src/app/loggingservice/api/gunicorn.config.py"]