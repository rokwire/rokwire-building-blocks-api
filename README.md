![Detect Secrets](https://github.com/rokwire/rokwire-building-blocks-api/workflows/Detect%20Secrets/badge.svg)

# Rokwire Platform Building Blocks API Documentation
API definitions of the Rokwire Platform building blocks

## Install commit hooks

```
$ pip install detect-secrets pre-commit
$ pre-commit install
```

## Setup and Run 

- Create the Rokwire Platform API Doc Docker image and run the Docker container:
        
      docker build -t rokwire/api-doc .
      docker run -p 80:8080 rokwire/api-doc 

  Now you can view the API documentation at http://localhost/docs/

## Docker / AWS ECR

Create Docker image for Rokwire Platform API and push to AWS ECR for deployment using Fargate from within AWS CLI:

```
docker build -t rokwire/api-doc .
docker tag rokwire/api-doc:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/api-doc:latest
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/api-doc:latest
```
