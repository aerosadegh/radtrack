#!/bin/sh
if [ -z "$DOCKER_MAINTAINER" ]; then
    export DOCKER_MAINTAINER="RadiaSoft <info@radiasoft.net>"
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
sh docker-test.sh
