#!/usr/bin/env bash

source release_base_script.sh

###### PROFILE BUILDING BLOCK ######
docker build --pull -f profileservice/Dockerfile -t ${PROJECT_NAME}/profile-building-block:${VERSION} .
docker tag ${PROJECT_NAME}/profile-building-block:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/profileservice:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/profileservice:${VERSION}
