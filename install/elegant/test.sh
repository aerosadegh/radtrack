#!/bin/sh
cd constructOrbitBump1
env RPN_DEFNS=/dev/null elegant run.ele &>/dev/null
if [ ! $? ]; then
    echo 'elegant failed to run' 1>&2
    exit 1
fi
