FROM python:3-alpine

LABEL maintainer="<ywkim@illinois.edu>, <wzhu26@illinois.edu>"

EXPOSE 5050

WORKDIR /usr/src/app/catalog

COPY catalog .

RUN pip install --upgrade pip && \
  pip install -r requirements.txt

WORKDIR /usr/src/app/catalog

ENV MONGO_CONTRIBUTION_URL="" \
    API_LOC="." \
    FLASK_APP="catalog_rest_service" \
    FLASK_ENV="development" \
    CATALOG_URL_PREFIX=""

CMD ["gunicorn", "catalog_rest_service:app", "--config", "/usr/src/app/catalog/gunicorn.config.py"]