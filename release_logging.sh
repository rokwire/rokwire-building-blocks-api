#!/usr/bin/env bash

source release_base_script.sh

###### LOGGING BUILDING BLOCK ######
docker build -f loggingservice/Dockerfile -t ${PROJECT_NAME}/logging-building-block:${VERSION} .
docker tag ${PROJECT_NAME}/logging-building-block:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/logging-building-block:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/logging-building-block:${VERSION}
