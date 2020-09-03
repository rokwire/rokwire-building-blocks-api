FROM python:3-alpine

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5050

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/catalog

COPY catalog .

RUN apk --update add python py-pip openssl ca-certificates py-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/contributions/api
#COPY rokwire.yaml .

ENV MONGO_CONTRIBUTION_URL="" \
    API_LOC="." \
    FLASK_APP="catalog_rest_service" \
    FLASK_ENV="development" \
    CATALOG_URL_PREFIX=""

CMD ["gunicorn", "catalog_rest_service:app", "--config", "/usr/src/app/catalog/gunicorn.config.py"]