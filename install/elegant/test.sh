#!/bin/sh
cd /cfg/constructOrbitBump1
if env RPN_DEFNS=/dev/null elegant run.ele &>/dev/null; then
    echo 'passed'
else
    echo 'failed' 1>&2
    exit 1
fi
