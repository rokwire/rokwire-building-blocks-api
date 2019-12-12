FROM python:3

LABEL maintainer="ywkim@illinois.edu"

EXPOSE 5000

WORKDIR /app

COPY loggingservice /app/loggingservice/

COPY lib /lib/

RUN pip install -r /app/loggingservice/requirements.txt

WORKDIR /app/loggingservice/api

RUN mv /lib .

COPY rokwire.yaml .

#ENV LOGGING_MONGO_URL=""
ENV LOGGING_URL_PREFIX="/logs"

CMD ["gunicorn", "loggingservice:create_app()", "--config", "/app/loggingservice/gunicorn.config.py"]

