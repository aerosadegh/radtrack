#!/bin/sh
if [ "x$(id -u)" != x0 ]; then
    echo 'Must be run as root' 1>&2
    exit 1
fi
if [ -z "$DOCKER_MAINTAINER" ]; then
    export DOCKER_MAINTAINER="RadiaSoft <info@radiasoft.net>"
fi
set -e
cd $(dirname $0)
image=radiasoft/elegant
read x1 x2 owner group x3 <<< "$(ls -adl .)"
tmp=.docker$$.build
rm -rf $tmp
mkdir $tmp
cp -a * $tmp
cd $tmp
log=err
echo "building: $image in $tmp/"
cat > Dockerfile <<EOF
FROM centos:centos6
MAINTAINER $DOCKER_MAINTAINER
ADD . /cfg
RUN sh /cfg/docker-install.sh
EOF

cat > docker-install.sh <<'EOF'
groupadd --gid 500 vagrant
useradd vagrant --uid 500 --gid vagrant --create-home
chmod -R a+rX /cfg
chown -R vagrant:vagrant /cfg
# centos6 seems to set terminal automatically to xterm so we have to unset prompts
cat <<'END' >> ~vagrant/.bashrc
export TERM=dumb
export PROMPT_COMMAND=
if [ ! -z "$PS1" ]; then
    export PS1='docker$ '
fi
END
sh /cfg/install.sh
EOF

chown -R $owner:$group .
docker rmi $image >&/dev/null || true
trap "cat $log" EXIT
docker build --tag=$image . &>>$log
name=elegant
docker rm $name &>/dev/null || true
docker run --name $name radiasoft/elegant su vagrant -c 'sh /cfg/test.sh'
docker rm $name &>>$log
trap '' EXIT
cd ..
rm -rf $tmp
