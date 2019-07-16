# Authentication Building Block

## dev notes

### to run locally

#### docker compose

- install docker
- `$ docker-compose up`

#### std python

- `$ python auth_rest_service.py`

### push docker image to repository

- `$ docker-compose build` or maybe `$ docker-compose build --no-cache --force-rm`
- `$ docker tag rokwire/authservice_web 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/authservice_web`
- `$ docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/authservice_web`
- if receive `denied: Your Authorization Token has expired. Please run 'aws ecr get-login --no-include-email' to fetch a new one.`
    - `$ $(aws ecr get-login --no-include-email --region us-east-2)`
