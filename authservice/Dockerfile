FROM python:3-alpine

LABEL maintainer="wzhu26@illinois.edu"

WORKDIR /app
COPY authservice /app/
COPY lib /lib/
COPY authservice/auth.yaml .

RUN apk --update add python py-pip openssl ca-certificates py-openssl && \
  apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt --no-cache-dir && \
  apk del build-dependencies

CMD ["gunicorn", "auth_rest_service:app", "--config", "/app/gunicorn.config.py"]
