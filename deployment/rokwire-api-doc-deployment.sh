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
[[ -n $matchingStarted ]] && sudo docker stop $matchingStarted

matching=$(sudo docker ps -a --filter="name=$name" -q | xargs)
[[ -n $matching ]] && sudo docker rm $matching

if [[ "$(sudo docker images -q swaggerapi/swagger-ui:latest 2> /dev/null)" == "" ]]; then
  sudo docker pull swaggerapi/swagger-ui
fi

sudo docker run --name=$name -p 80:8080 -p 8080:8080 -BASE_URL=/docs -e SWAGGER_JSON=/rokwire-api-doc/rokwire.yaml -v /home/ubuntu/rokwire-building-blocks-api:/rokwire-api-doc swaggerapi/swagger-ui&