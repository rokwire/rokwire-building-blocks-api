#!/usr/bin/env bash

source release_base_script.sh

# Contributions catalog version information
# Docker build args
gittag=$(git describe --tags $(git rev-list --tags --max-count=1) )
gitsha=$(git rev-parse --short HEAD)

###### CONTRIBUTIONS CATALOG ######
docker build --pull -f contributions/catalog/Dockerfile -t ${PROJECT_NAME}/contributions-catalog:${VERSION} --build-arg GIT_TAG=$gittag --build-arg GIT_SHA=$gitsha .
docker tag ${PROJECT_NAME}/contributions-catalog:${VERSION} 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/contributions-catalog:${VERSION}
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/${PROJECT_NAME}/contributions-catalog:${VERSION}