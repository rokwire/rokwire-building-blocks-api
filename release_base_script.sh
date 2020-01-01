#!/usr/bin/env bash

set -e

PROJECT_NAME="rokwire"
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "${GIT_BRANCH}" = "master" ]]; then
    VERSION=${VERSION:-"$(git describe --abbrev=0 --tags)"}
elif [[ "${GIT_BRANCH}" = "develop" ]]; then
    VERSION="develop"
elif [[ "${GIT_BRANCH}" = "feature/279-rokwire-platform-refactoring" ]]; then
    VERSION="279-refactor"
else
    exit 0
fi
