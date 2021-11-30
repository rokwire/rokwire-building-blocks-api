#!/usr/bin/env bash

source release_base_script.sh

###### APP CONFIG BUILDING BLOCK ######
docker build --pull -f appconfigservice/Dockerfile -t ${PROJECT_NAME}/app-config-building-block:${VERSION} .
docker tag ${PROJECT_NAME}/app-config-building-block:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/app_config:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/app_config:${VERSION}
