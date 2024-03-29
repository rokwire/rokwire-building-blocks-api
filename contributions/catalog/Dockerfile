FROM python:3.9-alpine

LABEL maintainers="minum@illinois.edu, sandeeps@illinois.edu"
LABEL authors="ywkim@illinois.edu, minum@illinois.edu"

WORKDIR /usr/src/app/catalog

COPY contributions/catalog .

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/catalog

ARG GIT_TAG
ARG GIT_SHA

ENV CONTRIBUTION_BUILDING_BLOCK_URL='' \
    DB_NAME='' \
    GITHUB_CLIENT_ID='' \
    GITHUB_CLIENT_SECRET='' \
    AUTHORIZATION_BASE_URL='https://github.com/login/oauth/authorize' \
    TOKEN_URL='https://github.com/login/oauth/access_token' \
    AUTHENTICATION_TOKEN='' \
    URL_PREFIX='/catalog' \
    DEBUG='False' \
    CATALOG_PORT=5000 \
    GIT_TAG=$GIT_TAG \
    GIT_SHA=$GIT_SHA

EXPOSE ${CATALOG_PORT}

CMD ["gunicorn", "catalog_rest_service:app", "--config", "/usr/src/app/catalog/gunicorn.config.py"]