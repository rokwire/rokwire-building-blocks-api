FROM python:3

LABEL maintainer="bing@illinois.edu"

RUN mkdir -p /app/eventservice/events-images/

WORKDIR /app
COPY rokwire.yaml /app/
COPY eventservice /app/eventservice/
COPY lib /lib/
RUN pip install -r /app/eventservice/requirements.txt

VOLUME /var/cache/app
WORKDIR /app/eventservice/api

CMD ["gunicorn", "events_rest_service:app", "--config", "/app/eventservice/api/gunicorn.config.py"]
