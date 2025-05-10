#!/bin/bash

# Script that starts the CSW services, compiles and runs the test assembly and then runs the python tests.
# Assumes that the virtual env (.venv) exists (created by `make all`),
# and assumes that cs, sbt, pytest are all in your shell path.

test -d .venv || { echo >&2 "Please run 'make' first to create .venv dir.  Aborting."; exit 1; }

# Make sure we can find sbt, cs
hash sbt 2>/dev/null || { echo >&2 "Please install sbt first.  Aborting."; exit 1; }
hash cs 2>/dev/null || { echo >&2 "Please install cs first.  Aborting."; exit 1; }
set -x

# Note: Make sure version matches ones used in csw/LocationService.py and tests/testSupport/project/Libs.scala
#CSW_VERSION=5.0.0
CSW_VERSION=6.0.0
CS_CHANNEL="https://raw.githubusercontent.com/tmtsoftware/osw-apps/branch-6.0.x/apps.json"
export PYTHONPATH=`pwd`

logfile=test.log
(cd tests/testSupport; sbt stage) > $logfile 2>&1
eval $(cs java --jvm temurin:1.21.0 --env)
cs launch --channel $CS_CHANNEL csw-services:$CSW_VERSION -- start -e -c >> $logfile 2>&1 &
sleep 60
tests/testSupport/test-deploy/target/universal/stage/bin/test-container-cmd-app --local tests/testSupport/test-deploy/src/main/resources/TestContainer.conf >> $logfile 2>&1 &
assemblyPid=$!
# give the background assembly time to initialize
sleep 5
# Run the python tests (add -s option to see stdout)
. .venv/bin/activate
pytest -rsx tests
kill $assemblyPid
# Kill csw-services
kill `ps aux | grep 'csw-services' | grep -v grep | awk '{print $2}'`
