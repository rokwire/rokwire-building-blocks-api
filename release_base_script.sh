#!/usr/bin/env bash

set -e

# Authenticate to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 779619664536.dkr.ecr.us-east-2.amazonaws.com

PROJECT_NAME="rokwire"
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "${GIT_BRANCH}" = "master" ]]; then
    VERSION=${VERSION:-"$(git describe --abbrev=0 --tags)"}
elif [[ "${GIT_BRANCH}" = "develop" ]]; then
    VERSION="develop"
else
    exit 0
fi
