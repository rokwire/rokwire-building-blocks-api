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

## Run docker in production

OS: Ubuntu 18.0.4
```
vi .bashrc
alias python=python3
alias pip=pip3
cd appconfigservice/deployment
./start_app_config_container.sh
./stop_app_config_container.sh

```
