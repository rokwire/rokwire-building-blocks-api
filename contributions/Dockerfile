FROM python:3-alpine3.12

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/contributions

COPY contributions .

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/contributions/api


COPY contributions/contribution.yaml .

ENV API_LOC='../' \
    MONGO_CONTRIBUTION_URL='localhost:27017' \
    FLASK_APP='contributions_rest_service' \
    FLASK_ENV='production' \
    CONTRIBUTION_URL_PREFIX='' \
    CONTRIBUTION_DB_NAME='contributions_db' \
    CONTRIBUTION_COLL_NAME='contributions' \
    DEBUG='False' \
    CORS_ENABLED='False'

CMD ["gunicorn", "contributions_rest_service:app", "--config", "/usr/src/app/contributions/api/gunicorn.config.py"]
