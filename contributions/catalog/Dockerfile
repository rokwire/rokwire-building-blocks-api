FROM python:3-alpine3.12

LABEL maintainer="<ywkim@illinois.edu>, <wzhu26@illinois.edu>"

EXPOSE 5050

WORKDIR /usr/src/app/catalog

COPY catalog .

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/catalog

ENV MONGO_CONTRIBUTION_URL="" \
    API_LOC="." \
    FLASK_APP="catalog_rest_service" \
    FLASK_ENV="development" \
    CATALOG_URL_PREFIX=""

CMD ["gunicorn", "catalog_rest_service:app", "--config", "/usr/src/app/catalog/gunicorn.config.py"]