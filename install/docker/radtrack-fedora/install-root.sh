#!/bin/sh
set -e
perl -pi -e '$. == 1 && ($_ .= "color=never\n")' /etc/yum.conf
rm -f /etc/profile.d/color*
cat >> /etc/bashrc <<'EOF'
export LOGNAME=${LOGNAME:-$(logname)}
if [ ! -z "$PS1" ]; then
    tty --silent && stty -echo
    x="$(compgen -a)"
    if [ ! -z "$x" ]; then
	unalias $x
    fi
    export LS_COLORS=
    export USER_LS_COLORS=
    export PROMPT_COMMAND=
    b_path_insert() {
	local dir="$1"
	local ignore_not_exist="$2"
	if [ \( "$ignore_not_exist" -o -d $dir \) -a $(expr ":$PATH:" : ".*:$dir:") = 0 ]; then
	    export PATH="$dir:$PATH"
	fi
    }
#TODO(robnagler): remove
    g() {
        local x="$1"
	shift
	grep -iIr "$x" ${@:-.}
    }
fi
EOF

cat >> /root/.bashrc <<'EOF'
export HOME=/root
cd $HOME
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi
test ! -z "$PS1" && export PS1='# '
EOF
