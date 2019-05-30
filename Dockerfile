FROM python:3-alpine

EXPOSE 5000

WORKDIR /usr/src/app

COPY profileservice/requirements.txt .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /usr/src/app/profileservice/restservice

ENV PROFILE_REST_STORAGE="/usr/src/app/rest" \
    PROFILE_MONGO_URL=""

CMD ["python", "profile_rest_service.py"]