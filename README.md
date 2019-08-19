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

- Create Rokwire Platform API Docker image using instructions in section `Docker / AWS ECR` and run:
        
      docker run -p 80:8080 rokwire/api-doc` 

  Then access the API doc at http://localhost/docs.

## Docker / AWS ECR

Create Docker image for Rokwire Platform API and push to AWS ECR for deployment using Fargate:

```
docker build -t rokwire/api-doc .
docker tag rokwire/api-doc:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/api-doc:latest
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/api-doc:latest
```

## AWS EC2 Deployment 

- Deploy api doc to AWS instance (created with Ubuntu Server 18.04 LTS image)
    
    ```
    cd /home/ubuntu
    git clone https://github.com/rokwire/rokwire-building-blocks-api.git
    
    ``` 
   
  Start docker container on AWS instance
 
    Make sure one of the security groups that the instance associated with, includes inbound rule accepting http requests from port 80 and 8080.

    ```
    cd /home/ubuntu/rokwire-building-blocks/deployment
    sh start_rokwire_apidoc_container.sh
    
    ```
  Stop and remove docker container on AWS instance
  
    ```
    cd /home/ubuntu/rokwire-building-blocks/deployment
    sh stop_rokwire_apidoc_container.sh
    
    ```


