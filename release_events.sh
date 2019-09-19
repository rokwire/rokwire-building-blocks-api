#!/usr/bin/env bash

source release_base_script.sh

###### PROFILE BUILDING BLOCK ######
docker build -f eventservice/Dockerfile -t ${PROJECT_NAME}/events-building-block:${VERSION} .
docker tag ${PROJECT_NAME}/events-building-block:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/eventservice:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/eventservice:${VERSION}
