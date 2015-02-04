#!/bin/sh
cd "$(dirname $0)"/constructOrbitBump1
cmd='elegant run.ele'
echo -n "running '$cmd': "
if env RPN_DEFNS=/dev/null $cmd &>/dev/null; then
    echo 'passed'
else
    echo 'failed' 1>&2
    exit 1
fi
