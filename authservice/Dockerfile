FROM python:3

LABEL maintainer="fhena2@illinois.edu"

WORKDIR /app
COPY . /app/
RUN pip install -r /app/requirements.txt

CMD ["gunicorn", "auth_rest_service:app", "--config", "/app/gunicorn.config.py"]
