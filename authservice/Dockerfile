FROM python:3-alpine3.12

LABEL maintainer="wzhu26@illinois.edu"

WORKDIR /app
COPY authservice /app/
COPY lib /lib/
COPY authservice/auth.yaml .

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip musl-dev cargo build-base && \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt --no-cache-dir && \
  apk del build-dependencies

CMD ["gunicorn", "auth_rest_service:app", "--config", "/app/gunicorn.config.py"]
