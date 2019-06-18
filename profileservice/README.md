# Profile Building Block

**profile rest service** is a Python project to provide rest service for rokwire building block profile
results.
                      

### Prerequisites

**MongoDB**

- A system must have a mongodb installed.

**[Python 3.5+](https://www.python.org)**


## Set Up

**MongoDB**
 
MongoDB should be installed

**Python**
Use requirements information

pip install -r requirements.txt

### Configuration
The necessary configuration should be configured in configure file (will be implemented later)

### Run application
Run ```python restservice/profile_rest_service.py``` and the profile building block should be running at http://localhost:5000
The detailed API information is in rokwire.yaml in the OpenAPI Spec 3.0 format.

## Use Dokcer
### Build a docker image
      docker build -t rokwire/profile-building-block .

### Test the docker container image:
      docker run --name profile-building-block -d --restart=always -e MONGO_PROFILE_URL=mongodb://<mongodb-url>:27017 -e MONGO_PII_URL=mongodb://<mongodb-url>:27017 -p 5000:5000 (-v /path/to/local/folder:/usr/src/app/rest) -d rokwire/profile-building-block
      
### To run without docker

This service uses the python Flask and pymongo libary.

To install and run the location-model service, do the following:

1. Setup a [virtualenv](https://virtualenv.pypa.io), e.g., named "rest-service":

   `virtualenv rest-service`
2. Activate the virtualenv

   `source rest-service/bin/activate`
3. Install required python packages using *pip*

   `pip install -r requirements.txt`

5. Modify mongo_url variable in config.py 

6. Start service, cd into /profileservice/restservice

   `python restservice/profile_rest_service.py`
