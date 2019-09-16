FROM python:3

LABEL maintainer="bing@illinois.edu"

ENV EVENT_MONGO_URL="" \
    EVENT_DB_NAME="" \
    URL_PREFIX=""

RUN mkdir -p /app/eventservice/events-images/

WORKDIR /app
COPY . /app/eventservice/
RUN pip install -r /app/eventservice/requirements.txt

CMD ["gunicorn", "eventservice:create_app()", "--config", "/app/eventservice/gunicorn.config.py"]
