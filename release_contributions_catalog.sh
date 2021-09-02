#!/usr/bin/env bash

source release_base_script.sh

###### CONTRIBUTIONS BUILDING BLOCK ######
docker build --pull -f contributions/Dockerfile -t ${PROJECT_NAME}/contributions-catalog:${VERSION} .
docker tag ${PROJECT_NAME}/contributions-catalog:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/contributions-catalog:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/contributions-catalog:${VERSION}
