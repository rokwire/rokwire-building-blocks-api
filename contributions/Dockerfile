FROM python:3-alpine

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/contributions

COPY contributions .

RUN apk --update add python py-pip openssl ca-certificates py-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/contributions/api

COPY contributions/contribution.yaml .

ENV MONGO_CONTRIBUTION_URL="" \
    API_LOC="." \
    FLASK_APP="contributions_rest_service" \
    FLASK_ENV="development" \
    CONTRIBUTION_URL_PREFIX=""

CMD ["gunicorn", "contributions_rest_service:app", "--config", "/usr/src/app/contributions/api/gunicorn.config.py"]
