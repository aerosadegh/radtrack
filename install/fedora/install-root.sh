#!/bin/sh
set -e
export HOME=/root
cp -a /etc/skel/.??* /root
cat > /.bashrc << 'EOF'
export HOME=/root
cd $HOME
. /root/.bash_profile
EOF

cat > $HOME/.post.bashrc <<'EOF'
tty --silent && stty -echo
EOF

curl –s -L https://raw.githubusercontent.com/biviosoftware/home-env/master/install.sh | bash
