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
