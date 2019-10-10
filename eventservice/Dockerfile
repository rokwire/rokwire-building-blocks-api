FROM python:3

LABEL maintainer="bing@illinois.edu"

RUN mkdir -p /app/eventservice/events-images/

WORKDIR /app
COPY eventservice /app/eventservice/
COPY lib /lib/
RUN pip install -r /app/eventservice/requirements.txt

VOLUME /var/cache/app

CMD ["gunicorn", "eventservice:create_app()", "--config", "/app/eventservice/gunicorn.config.py"]
