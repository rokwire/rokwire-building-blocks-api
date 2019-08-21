FROM python:3

LABEL maintainer="ywkim@illinois.edu"

WORKDIR /app
COPY . /app/loggingservice/
RUN pip install -r /app/loggingservice/requirements.txt

# For using DocumentDB
RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

ENV LOGGING_MONGO_URL=""
ENV LOGGING_URL_PREFIX="/logs"

CMD ["gunicorn", "loggingservice:create_app()", "--config", "/app/loggingservice/gunicorn.config.py"]
