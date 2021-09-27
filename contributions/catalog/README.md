# Contribution Catalog 

### Prerequisites

**MongoDB**

- A system must have a mongodb installed.

**[Python 3.5+](https://www.python.org)**


## Set Up

**MongoDB**
 
 MongoDB should be installed

**Configuration**

The necessary configuration should be configured in configure file (configs.py) that is located under profileservice folder. This contains the MongoDB url, database name, collection name and so on. Modify the information in the file appropriately.

## Environment File

You need to have a `.env` file in this directory that contains credentials required for authentication. 
Not all of these variables may be required for this building block.

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
docker run --name catalog --rm --env-file=contributions/catalog/.env -e MONGO_URL=mongodb://<mongodb-url>:27017 -p 5000:5000 rokwire/contributions-catalog
```

For a list of available configurations, please see `controllers/config.py`.


### AWS ECR Instructions

Make sure that a repository called rokwire/contributions-catalog exists in ECR. Then, create the Docker image for Contributions Catalog and push to AWS ECR using:

```
cd rokwire-building-blocks-api
$(aws ecr get-login --no-include-email --region us-east-2)
docker build --pull -f contributions/catalog/Dockerfile -t rokwire/contributions-catalog .
docker tag rokwire/contributions-catalog:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/contributions-catalog:latest
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/contributions-catalog:latest
```