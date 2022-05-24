#!/usr/bin/env bash

source release_base_script.sh

###### CONTRIBUTIONS BUILDING BLOCK ######
docker build --no-cache --pull -f contributions/Dockerfile -t ${PROJECT_NAME}/contributions-building-block:${VERSION} .
docker tag ${PROJECT_NAME}/contributions-building-block:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/contributions-building-block:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/contributions-building-block:${VERSION}
