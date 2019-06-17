FROM python:3-alpine

EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && \
  pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del build-dependencies

COPY . .

WORKDIR /usr/src/app/restservice

ENV PROFILE_REST_STORAGE="/usr/src/app/rest" \
    MONGO_PROFILE_URL="" \
    MONGO_PII_URL=""

CMD ["python", "profile_rest_service.py"]