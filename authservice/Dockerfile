FROM python:3

LABEL maintainer="fhena2@illinois.edu"

WORKDIR /app
COPY authservice /app/
COPY lib /lib/
RUN pip install -r /app/requirements.txt

CMD ["gunicorn", "auth_rest_service:app", "--config", "/app/gunicorn.config.py"]
