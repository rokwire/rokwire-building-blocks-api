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

Using cURL to interact with API running on local host:
```

curl -H "Content-Type: application/json" -d '{"mobileAppVersion": "0.1.0", "platformBuildingBlocks": {}, "thirdPartyServices": {}, "otherUniversityServices": {}}' -X POST http://localhost:5000/app/configs   

curl -X GET http://localhost:5000/app/configs 

curl -X DELETE http://localhost:5000/app/configs/5d27858e633c14d86da2ee0c

curl -H "Content-Type: application/json" -d '{"mobileAppVersion": "0.1.0", "platformBuildingBlocks": {"appconfig": "http://api.rokwire.illinois.edu/app/configs"}, "thirdPartyServices": {}, "otherUniversityServices": {}}' -X PUT http://localhost:5000/app/configs/5d278c719725c37c8c811e2a 

curl -X GET http://localhost:5000/app/configs/5d278c719725c37c8c811e2a

```

Using cURL and a JSON data file to create app configuration on API running on dev server:

```

curl -d "@appconfig-v094.json" -X POST https://api-dev.rokwire.illinois.edu/app/configs

```

## Run docker in production

1. Create EC2 instance with Ubuntu 18.0.4 AMI
2. Install mongodb if needed
3. Install pip3
4. More instructions:

```
vi .bash_aliases
alias python=python3
alias pip=pip3
sudo apt-get install docker.io
cd appconfigservice
./build_app_config.sh
cd ../deployment
./start_app_config_container.sh
./stop_app_config_container.sh

```
