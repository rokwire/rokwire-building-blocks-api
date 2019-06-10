#!/bin/bash

# deploy rokwire API doc
sudo apt update
if [ -x "$(command -v docker)" ]; then
    echo "Update docker"
else
    echo "Install docker"
    #install docker from Ubuntu repository
    sudo apt install docker.io
fi

name="rokwire-api-doc"

matchingStarted=$(sudo docker ps --filter="name=$name" -q | xargs)
if [ ! -z $matchingStarted ]; then 
    echo "stop docker"
    sudo docker stop $matchingStarted
fi

matching=$(sudo docker ps -a --filter="name=$name" -q | xargs)
if [ ! -z $matching ]; then
    echo "rm docker"
    sudo docker rm $matching
fi

swaggerImage="swaggerapi/swagger-ui:latest"

matchingImage=$(sudo docker images -q $swaggerImage -q | xargs)
if [ -z $matchingImage ]; then
  echo "pull swagger docker image"
  sudo docker pull swaggerapi/swagger-ui
fi

sudo docker run --name=$name -p 80:8080 -p 8080:8080 -e BASE_URL=/docs -e SWAGGER_JSON=/rokwire-api-doc/rokwire.yaml -v /home/ubuntu/rokwire-building-blocks-api:/rokwire-api-doc swaggerapi/swagger-ui&
