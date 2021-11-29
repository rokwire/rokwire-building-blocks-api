# Contribution Catalog 

### Prerequisites

**MongoDB**

- A system must have a mongodb installed.

**[Python 3.5+](https://www.python.org)**


## Set Up

**MongoDB**
 
 MongoDB should be installed

**Configuration**

All configurations can be found in the configuration file (configs.py) that is located under the `controllers` folder.

## Environment File

You need to have a `.env` file in this directory that contains credentials required for authentication. 
Other configuration items can also be added to the `.env` file.

Example .env file:

```shell
ROKWIRE_API_KEY=<ROKWIRE_API_KEY> # Rokwire API key.
FLASK_ENV=<development> # Flask runtime environment.
DEBUG=True # Boolean to enable/disable debug mode.
GITHUB_CLIENT_ID=<GitHub Client ID> # GitHub OAuth App client ID.
GITHUB_CLIENT_SECRET=<GitHub Client Secret> # pragma: allowlist secret. GitHub OAuth App client secret.
SECRET_KEY=<SECRET_KEY> # A secret key that will be used for securely signing the session cookies.
ADMIN_USERS=<GitHub username1, GitHub username2>
CATALOG_PORT=<Port> # Port to run the Contributions Catalog (default: 5000).
```

## Run application

### Run locally without Docker

This service uses the python Flask and PyMongo library.

The configuration file configs.py should have the appropriate information

To install and run the location-model service, do the following:

## Setup Environment and start the catalog application
- (Linux or MAC):
```
cd contributions/catalog
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
set FLASK_APP=catalog
set FLASK_ENV=development
python catalog_rest_service.py
```
- (Windows):
```
cd contributions/catalog
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=catalog
set FLASK_ENV=development
python catalog_rest_service.py
```
If you want to use gunicorn, cd into api folder then, use ` gunicorn catalog_rest_service:app -c gunicorn.config.py` instead of `python catalog_rest_service.py`


### Run using Docker

```
cd rokwire-building-blocks-api
docker build --pull -f contributions/catalog/Dockerfile -t rokwire/contributions-catalog .
docker run --name catalog --rm --env-file=contributions/catalog/.env -e MONGO_URL=mongodb://<mongodb-url>:27017 -p 5050:5000 rokwire/contributions-catalog

For a list of available configurations, please see `controllers/config.py`.


### AWS ECR Instructions

Make sure that a repository called rokwire/contributions-catalog exists in ECR. Then, create the Docker image for Contributions Catalog and push to AWS ECR using:

```
cd rokwire-building-blocks-api
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 779619664536.dkr.ecr.us-east-2.amazonaws.com
docker build --pull -f contributions/catalog/Dockerfile -t rokwire/contributions-catalog .
docker tag rokwire/contributions-catalog:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/contributions-catalog:latest
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/contributions-catalog:latest
```