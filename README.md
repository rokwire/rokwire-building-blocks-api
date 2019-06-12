# Rokwire Building Blocks API
API definitions of the Rokwire Platform building blocks

## How to view API design doc 

There are several ways to view API design and document using Swagger:

- Go to [Swagger UI demo page](https://petstore.swagger.io/) and paste [Rokwire API YAML file URL](https://raw.githubusercontent.com/rokwire/rokwire-building-blocks-api/develop/rokwire.yaml) there.

- Sign up a free account at [SwaggerHub](https://swagger.io/tools/swaggerhub/) and create new API by importing your copy of rokwire.yaml file.

- Get swagger docker image, for example 

      docker pull swaggerapi/swagger-ui 

  Run docker image locally by executing command like 

      docker run -p 80:8080 -e SWAGGER_JSON=/foo/rokwire.yaml -v /rokwire_yaml_local_dir/:/foo -e BASE_URL=/docs swaggerapi/swagger-ui 

  Then access the API doc at http://localhost/docs. 

- Deploy api doc to AWS instance (created with Ubuntu Server 18.04 LTS image)
    
    ```
    cd /home/ubuntu
    git clone https://github.com/rokwire/rokwire-building-blocks-api.git
    
    ``` 
   
  Start docker container on AWS instance
 
    Make sure one of the security groups that the instance associated with, includes inbound rule accepting http requests from port 80 and 8080.

    ```
    cd /home/ubuntu/rokwire-building-blocks
    sh start_rokwire_apidoc_container.sh
    
    ```
  Stop and remove docker container on AWS instance
  
    ```
    cd /home/ubuntu/rokwire-building-blocks
    sh start_rokwire_apidoc_container.sh
    
    ```
    
## Build a docker image
      docker build -t rokwire/profiles .

## Test the docker container image:
      docker run --name profiles-rest-service -d --restart=always -e MONGO_URL=mongodb://<mongodb-url>:27017 -p 5000:5000 -v /home/ywkim/rest:/usr/src/app/rest -d rokwire/profiles
      
## To run without docker

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

   `./profile_rest_service.py`


