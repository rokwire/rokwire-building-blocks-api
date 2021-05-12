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

ENV MONGO_CONTRIBUTION_URL='' \
    API_LOC='../' \
    FLASK_APP='contributions_rest_service' \
    FLASK_ENV='production' \
    MONGO_CONTRIBUTION_URL='localhost:27017' \
    CONTRIBUTION_URL_PREFIX='' \
    CONTRIBUTION_URL_PREFIX='CONTRIBUTION_URL_PREFIX' \
    CONTRIBUTION_DB_NAME='' \
    CONTRIBUTION_COLL_NAME='' \
    CAPABILITY_COLL_NAME='' \
    CONTRIBUTION_BUILDING_BLOCK_URL='' \
    FIELD_OBJECTID='' \
    FIELD_NAME='' \
    GITHUB_CLIENT_ID='' \
    GITHUB_CLIENT_SECRET='' \
    authorization_base_url='https://github.com/login/oauth/authorize' \
    token_url='https://github.com/login/oauth/access_token' \
    ROKWIRE_API_KEY='' \
    URL_PREFIX='' \
    DEBUG='False' \
    CORS_ENABLED='False'

CMD ["gunicorn", "contributions_rest_service:app", "--config", "/usr/src/app/contributions/api/gunicorn.config.py"]
