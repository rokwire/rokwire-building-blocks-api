FROM python:3-alpine

EXPOSE 5000

WORKDIR /usr/src/app

COPY profileservice/requirements.txt .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /usr/src/app/profileservice/restservice

CMD ["python", "profile_rest_service.py"]