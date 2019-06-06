FROM python:3

LABEL maintainer="bing@illinois.edu"

WORKDIR /app
COPY . /app/eventservice/
RUN pip install -r /app/eventservice/requirements.txt

#CMD [ "gunicorn", "-n events", "-w 4", "-b 0.0.0.0:5000", "eventservice:create_app()"]
CMD ["gunicorn", "eventservice:create_app()", "--config", "/app/eventservice/gunicorn.config.py"]