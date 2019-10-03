#!/usr/bin/env bash

source release_base_script.sh

###### API DOCUMENTATION ######
docker build -t ${PROJECT_NAME}/api-doc:${VERSION} .
docker tag ${PROJECT_NAME}/api-doc:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/api-doc:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/api-doc:${VERSION}
