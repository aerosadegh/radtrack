#!/bin/sh
name=elegant$$
echo -n 'test: '
docker run --name $name radiasoft/elegant sh /cfg/test.sh
docker rm $name &>/dev/null

