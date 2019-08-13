FROM python:3

LABEL maintainer="ywkim@illinois.edu"

WORKDIR /app
COPY . /app/loggingservice/
RUN pip install -r /app/loggingservice/requirements.txt

CMD ["gunicorn", "loggingservice:create_app()", "--config", "/app/loggingservice/gunicorn.config.py"]
