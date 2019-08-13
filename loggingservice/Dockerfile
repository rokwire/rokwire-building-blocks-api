FROM python:3

LABEL maintainer="ywkim@illinois.edu"

WORKDIR /app
COPY . /app/eventservice/
RUN pip install -r /app/eventservice/requirements.txt

CMD ["gunicorn", "loggingservice:create_app()", "--config", "/app/loggingservice/gunicorn.config.py"]
