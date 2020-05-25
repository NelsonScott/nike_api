#!/usr/bin/env bash

set -euxo pipefail

IMG_NAME=nike_api
docker build . -t $IMG_NAME
docker run -v $(pwd):/${PWD##*/} -w /${PWD##*/} $IMG_NAME bash -c "./get_workouts.py"
