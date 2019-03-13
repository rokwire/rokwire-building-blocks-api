# rokwire-core-services-api
API definitions of the Rokwire Platform core services

## How to view API design doc 
There are several ways to view API design and document using Swagger:

- Go to Swagger UI demo page (https://petstore.swagger.io/) and paste our YAML file URL there (https://raw.githubusercontent.com/rokwire/scci-core-services-api/develop/rokwire.yaml).

- Sign up a free account at [SwaggerHub](https://swagger.io/tools/swaggerhub/) and "Create New" API by importing your copy of rokwire.yaml file.

- Get swagger docker image, for example, "docker pull swaggerapi/swagger-ui" and run docker image locally by executing command like "docker run -p 80:8080 -e SWAGGER_JSON=/foo/rokwire.yaml -v /rokwire_yaml_local_dir/:/foo -e BASE_URL=/docs swaggerapi/swagger-ui. Then access the API doc at http://localhost/docs.  
