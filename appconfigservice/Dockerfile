FROM python:3-stretch

LABEL maintainer="sandeeps@illinois.edu"

WORKDIR /app

COPY appconfigservice/app /app
COPY appconfigservice/requirements.txt /app/requirements.txt
COPY appconfigservice/gunicorn.config.py /app/gunicorn.config.py
COPY lib /lib/

ENV APP_CONFIG_MONGO_URL=""

RUN pip install -r /app/requirements.txt

# For using DocumentDB
RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

CMD ["gunicorn", "appconfig:create_app()", "--config", "/app/gunicorn.config.py"]
