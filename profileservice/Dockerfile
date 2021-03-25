FROM python:3-alpine3.12

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/profileservice

COPY profileservice .

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/profileservice/api

COPY profileservice/profile.yaml .

ENV PROFILE_REST_STORAGE="/usr/src/app/rest" \
    MONGO_PROFILE_URL="" \
    MONGO_PII_URL="" \
    API_LOC="." \
    FLASK_APP="profile_rest_service" \
    FLASK_ENV="development" \
    PROFILE_URL_PREFIX=""

CMD ["gunicorn", "profile_rest_service:app", "--config", "/usr/src/app/profileservice/api/gunicorn.config.py"]
