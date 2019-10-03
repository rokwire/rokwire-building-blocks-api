#!/usr/bin/env bash

source release_base_script.sh

###### AUTHENTICATION BUILDING BLOCK ######
docker build -f authservice/Dockerfile -t ${PROJECT_NAME}/authentication-building-block:${VERSION} .
docker tag ${PROJECT_NAME}/authentication-building-block:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/authservice_web:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/authservice_web:${VERSION}
