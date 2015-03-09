#!/bin/sh
IMAGE=radiasoft/radtrack-py2
docker rmi $IMAGE
docker build --rm=true --tag=$IMAGE .
