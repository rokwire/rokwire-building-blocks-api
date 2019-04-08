#!/bin/bash
set -e

# start server if asked
if [ "$1" = 'location-model' ]; then
    # just launch extractor and see what happens
    exec ./${MAIN_SCRIPT}
fi

exec "$@"