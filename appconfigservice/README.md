# App Config Building Block

The goal of the App Config Building Block is to provide a set of RESTFul web services to manage app configuration in the Rokwire platform. 
Please see API documentation for more details at https://api.rokwire.illinois.edu/docs/
                      

## Getting Started
#### Requirements
- **MongoDB** installed
- **[Python 3.5+](https://www.python.org)**

#### Set up Environment File
We need to have a .env file in this directory that contains credentials required for authentication. 
Not all of these variables may be required for this building block. 

Example `.env` file format:
```
TWILIO_ACCT_SID=<Twilio Account SID>
TWILIO_AUTH_TOKEN=<Twilio Auth Token>
TWILIO_VERIFY_SERVICE_ID=<Twilio Verify Service ID>

PHONE_VERIFY_SECRET=<Phone Verify Secret> 
PHONE_VERIFY_AUDIENCE=<Phone Verify Audience>

SHIBBOLETH_HOST=<Shibboleth Host Name>
SHIBBOLETH_CLIENT_ID=<Shibboleth Client ID>

ROKWIRE_API_KEY=<Rokwire API Key>
ROKWIRE_ISSUER=<Rokwire ID Token Issuer Name>
ROKWIRE_PUB_KEY=<Rokwire Public Key>
ROKWIRE_API_CLIENT_ID=<Rokwire API Client ID>
```



### Run in Development Mode without Docker
To setup environment:
```
cd appconfigservice
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
And run AppConfig module:
```
source venv/bin/activate
export FLASK_ENV=development
python api/appconfig_rest_service.py
```

### API Examples
Using Postman to interact with the API (i.e. `GET/POST/PUT/DELETE`):

1. Set up authorization in Header
    - ApiKeyAuth: `ROKWIRE_API_KEY:<Rokwire API Key> (as in .env file)`
    - UserAuth: `Authorization:bearer+<Phone Verify Secret>` or `Authorization:bearer+<ID Token>` 
    
2. Send requests
- POST
    - URL: `http://localhost:5000/app/configs`
    - Header: `Content-Type: application/json`
    - Body: `{"mobileAppVersion": "0.1.0", "platformBuildingBlocks": {"events_url": "https://api-dev.rokwire.illinois.edu/events"}, "thirdPartyServices": {"instagram_host_url": "https://instagram.com/"}, "otherUniversityServices": {"illini_cash_base_url": "https://shibtest.housing.illinois.edu/MobileAppWS/api"}, "secretKeys": "", "upgrade": {}} `
    - UserAuth
    
- GET
    - URL: `http://localhost:5000/app/configs`
    - ApiKeyAuth

- GET by query
    - URL: `http://localhost:5000/app/configs?mobileAppVersion=0.1.0`
    - ApiKeyAuth

- PUT
    - URL : `http://localhost:5000/app/configs/5d278c719725c37c8c811e2a`
    - Header: `Content-Type: application/json`
    - Body: `{"mobileAppVersion": "0.1.0", "platformBuildingBlocks": {"events_url": "https://api-dev.rokwire.illinois.edu/events", "appconfig": "http://api.rokwire.illinois.edu/app/configs"}, "thirdPartyServices": {"instagram_host_url": "https://instagram.com/", "twitter_host_url": "https://twitter.com/"}, "otherUniversityServices": {"illini_cash_base_url": "https://shibtest.housing.illinois.edu/MobileAppWS/api", "privacy_policy_url": "https://www.vpaa.uillinois.edu/resources/web_privacy"}, "secretKeys": {'xx-key': "1234abcd#7890efg"}}`
    - UserAuth 
    
- GET by ID
    - URL : `http://localhost:5000/app/configs/5d278c719725c37c8c811e2a`
    - UserAuth

- DELETE
    - URL : `http://localhost:5000/app/configs/5d27858e633c14d86da2ee0c`
    - UserAuth


We can also use cURL and a JSON file to create or update the API:

```
curl -d "@appconfig-v094.json" -X POST http://localhost:5000/app/configs
curl -d "@appconfig-v100.json" -X PUT http://localhost:5000/app/configs/5d38b9a566933ef80c76203b

```

## Docker Run Instructions

```
cd rokwire-building-blocks-api 
docker build -f appconfigservice/Dockerfile -t rokwire/app-config-building-block:latest .
docker run --rm --name app_config --env-file appconfigservice/.env -e APP_CONFIG_MONGO_URL=<mongo_url> -p 5000:5000 rokwire/app-config-building-block
```
where `<mongo_url> =mongodb://localhost:27017` is in current setting

## AWS ECR Instructions

Make sure the repository called rokwire/app_config exists in ECR. 
Then create Docker image for Rokwire Platform API and push to AWS ECR for deployment. 
For example:

```
cd rokwire-building-blocks-api 
docker build -f appconfigservice/Dockerfile -t rokwire/app-config-building-block:latest .
docker tag rokwire/app-config-building-block:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/app_config:latest
$(aws ecr get-login --no-include-email --region us-east-2)
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/app_config:latest
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
