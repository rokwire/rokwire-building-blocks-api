#!/usr/bin/env bash

set -e

PROJECT_NAME="rokwire"
VERSION="latest"

docker build --pull -f appconfigservice/Dockerfile -t ${PROJECT_NAME}/app-config-building-block:${VERSION} .
docker build --pull -f authservice/Dockerfile -t ${PROJECT_NAME}/authentication-building-block:${VERSION} .
docker build --pull -f loggingservice/Dockerfile -t ${PROJECT_NAME}/logging-building-block:${VERSION} .
docker build --pull -f eventservice/Dockerfile -t ${PROJECT_NAME}/events-building-block:${VERSION} .
docker build --pull -f profileservice/Dockerfile -t ${PROJECT_NAME}/profile-building-block:${VERSION} .
