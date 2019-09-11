# App Config Building Block

The goal of the App Config Building Block is to provide a set of RESTFul web services to manage app configuration in the Rokwire platform. 
Please see API documentation for more details at https://api.rokwire.illinois.edu/docs/
                      

## Setup Environment
```
cd appconfigservice
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Unit tests
```
cd appconfigservice
pip install '.[test]'
pytest
```

## Build and install   
```
cd appconfigservice
pip install -e .
```

## Environment File

You need to have a .env file in this directory that contains credentials required for authentication. 
Not all of these variables may be required for this building block. 

Example file format:

```
TWILIO_ACCT_SID=<Twilio Account SID>
TWILIO_AUTH_TOKEN=<Twilio Auth Token>
TWILIO_VERIFY_SERVICE_ID=<Twilio Verify Service ID>

PHONE_VERIFY_SECRET=<Phone Verify Secret> 
PHONE_VERIFY_AUDIENCE=<Phone Verify Audience>

SHIBBOLETH_HOST=<Shibboleth Host Name>
SHIBBOLETH_CLIENT_ID=<Shibboleth Client ID>

ROKWIRE_API_KEY=<Rokwire API Key>
```

## Run in Development Mode
```
cd appconfigservice
export FLASK_APP=appconfig
export FLASK_ENV=development
flask run
```

## API Usage Examples

Using cURL to interact with the API:
```

curl -H "Content-Type: application/json" -d '{"mobileAppVersion": "0.1.0", "platformBuildingBlocks": {"events_url": "https://api-dev.rokwire.illinois.edu/events"}, "thirdPartyServices": {"instagram_host_url": "https://instagram.com/"}, "otherUniversityServices": {"illini_cash_base_url": "https://shibtest.housing.illinois.edu/MobileAppWS/api"}, "secretKeys": {}}' -X POST http://localhost:5000/app/configs   

curl -X GET http://localhost:5000/app/configs 

curl -X DELETE http://localhost:5000/app/configs/5d27858e633c14d86da2ee0c

curl -H "Content-Type: application/json" -d '{"mobileAppVersion": "0.1.0", "platformBuildingBlocks": {"events_url": "https://api-dev.rokwire.illinois.edu/events", "appconfig": "http://api.rokwire.illinois.edu/app/configs"}, "thirdPartyServices": {"instagram_host_url": "https://instagram.com/", "twitter_host_url": "https://twitter.com/"}, "otherUniversityServices": {"illini_cash_base_url": "https://shibtest.housing.illinois.edu/MobileAppWS/api", "privacy_policy_url": "https://www.vpaa.uillinois.edu/resources/web_privacy"}, "secretKeys": {'xx-key': "1234abcd#7890efg"}}' -X PUT http://localhost:5000/app/configs/5d278c719725c37c8c811e2a 

curl -X GET http://localhost:5000/app/configs/5d278c719725c37c8c811e2a

curl -X GET http://localhost:5000/app/configs?mobileAppVersion=1.0.0

```

Using cURL and a JSON data file to create or update the API:

```

curl -d "@appconfig-v094.json" -X POST http://localhost:5000/app/configs
curl -d "@appconfig-v100.json" -X PUT http://localhost:5000/app/configs/5d38b9a566933ef80c76203b

```

## Run docker in a VM

OS: Ubuntu 18.0.4
```
vi .bashrc
alias python=python3
alias pip=pip3
cd rokwire-building-blocks-api/deployment
./start_app_config_container.sh
./stop_app_config_container.sh

```

## Docker Instructions

```
cd rokwire-building-blocks-api 
docker build -f appconfigservice/Dockerfile -t rokwire/app-config-building-block:latest .
cd appconfigservice
docker run --rm --name app_config --env-file .env -e APP_CONFIG_MONGO_URL=<mongo_url> -p 5000:5000 rokwire/app-config-building-block
```

## AWS ECR Instructions

Make sure the repository called rokwire/app_config exists in ECR. Then create Docker image for Rokwire Platform API and push to AWS ECR for deployment. For

```
cd rokwire-building-blocks-api 
docker build -f appconfigservice/Dockerfile -t rokwire/app-config-building-block:latest .
docker tag rokwire/app-config-building-block:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/app_config:latest
$(aws ecr get-login --no-include-email --region us-east-2)
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/app_config:latest
```
