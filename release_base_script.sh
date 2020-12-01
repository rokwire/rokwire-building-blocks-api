#!/usr/bin/env bash

set -e

PROJECT_NAME="rokwire"
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "${GIT_BRANCH}" = "master" ]]; then
    VERSION=${VERSION:-"$(git describe --abbrev=0 --tags)"}
elif [[ "${GIT_BRANCH}" = "develop" ]]; then
    VERSION="develop"
elif [[ "${GIT_BRANCH}" = "group-events/master" ]]; then
    VERSION=${VERSION:-"group-events-$(git describe --abbrev=0 --tags)"}
elif [[ "${GIT_BRANCH}" = "group-events/develop" ]]; then
    VERSION="group-events-develop"
else
    exit 0
fi
