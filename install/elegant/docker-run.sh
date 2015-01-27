#!/bin/sh
if [ "x$(id -u)" != x0 ]; then
    echo 'Must be run as root' 1>&2
    exit 1
fi
name="$(basename $(pwd))"
set -e
if docker ps -a | grep -q -s " $name "; then
    echo "Existing container: $name"
    docker start --attach --interactive $name
else
    echo "New container: $name"
    docker run --interactive --tty --name $name radiasoft/$name su - vagrant
fi
echo "Exitted container: $name"
echo "To delete this container: docker rm $name"
