#!/bin/sh
if [ -z "$DOCKER_MAINTAINER" ]; then
    echo 'you must supply $DOCKER_MAINTAINER' 1>&2
    exit 1
fi
IMAGE=radiasoft/elegant
cat > Dockerfile <<EOF
FROM centos:centos6
MAINTAINER $DOCKER_MAINTAINER
ADD . /cfg
RUN sh /cfg/docker-install.sh
EOF

docker rmi $IMAGE
docker build --tag=$IMAGE .
