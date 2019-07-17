# Authentication Building Block

## usage

### Step 1 - phone-initiate

Step 1 of 2 for phone number verification. Initiates the verification with a text or call that contains a code. That code should then be provided to the /authentication/phone-verify endpoint. Note: The phoneNumber property must include a prefix plus symbol (+), the country code (e.g., 1 for USA), and the area code.

#### example

    curl -d '{
               "phoneNumber": "+12175557890",
               "channel": "sms"
    }' -H "Content-Type: application/json" -X POST https://api-dev.rokwire.illinois.edu/authentication/phone-initiate

### Step 2 - phone-verify

Step 2 of 2 for phone number verification. The request body should contain the code that was sent to the end user as a result of the /authentication/phone-initiate endpoint. phone-verify will check if the code matches what was originally sent to the user. Note: The phoneNumber property must include a prefix plus symbol (+), the country code (e.g., 1 for USA), and the area code.

#### example

    curl -d '{
               "phoneNumber": "+12175557890",
               "code": "974010"
    }' -H "Content-Type: application/json" -X POST https://api-dev.rokwire.illinois.edu/authentication/phone-verify

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
