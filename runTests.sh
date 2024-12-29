#!/bin/bash

# Script that starts the CSW services, compiles and runs the test assembly and then runs the python tests.
# Assumes that the virtual env (.venv) exists (created by `make all`),
# and assumes that cs, sbt, pytest are all in your shell path.

test -d .venv || { echo >&2 "Please run 'make' first to create .venv dir.  Aborting."; exit 1; }
. .venv/bin/activate

# Make sure we can find sbt, cs
hash sbt 2>/dev/null || { echo >&2 "Please install sbt first.  Aborting."; exit 1; }
hash cs 2>/dev/null || { echo >&2 "Please install cs first.  Aborting."; exit 1; }

# Note: Make sure version matches ones used in csw/LocationService.py and tests/testSupport/project/Libs.scala
#CSW_VERSION=5.0.0
CSW_VERSION=919e345
CS_CHANNEL="https://raw.githubusercontent.com/tmtsoftware/osw-apps/Allan/pekko-scala3-update-esw-http-api/apps.json"

logfile=test.log
set -x
eval $(cs java --jvm temurin:1.21.0 --env)
cs launch --channel $CS_CHANNEL csw-services:$CSW_VERSION -- start -e -c -k > $logfile 2>&1 &
cd tests/testSupport || exit 1
sbt clean stage  >> $logfile 2>&1
test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf   >> $logfile 2>&1 &
assemblyPid=$!
cd ../..
export PYTHONPATH=`pwd`
# give the background assembly time to initialize
sleep 10
# Run the python tests (add -s option to see stdout)
pytest -rsx tests
kill $assemblyPid
# Kill csw-services
kill `ps aux | grep 'csw-services' | grep -v grep | awk '{print $2}'`
