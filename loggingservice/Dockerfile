FROM python:3-alpine

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5000

WORKDIR /usr/src/app/lib

COPY lib .

WORKDIR /usr/src/app/loggingservice

COPY loggingservice .

RUN pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir 

WORKDIR /usr/src/app/loggingservice/api

COPY rokwire.yaml .

#ENV LOGGING_MONGO_URL=""
ENV LOGGING_URL_PREFIX="/logs"

CMD ["gunicorn", "logging_rest_service:app", "--config", "/usr/src/app/loggingservice/api/gunicorn.config.py"]