FROM python:3-alpine

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/profileservice

COPY profileservice .

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

WORKDIR /usr/src/app/profileservice/restservice

RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

ENV PROFILE_REST_STORAGE="/usr/src/app/rest" \
    MONGO_PROFILE_URL="" \
    MONGO_PII_URL="" \
    FLASK_APP="profile_rest_service" \
    FLASK_ENV="development"

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]