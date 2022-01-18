#!/bin/bash

# Script that starts the CSW services, compiles and runs the test assembly and then runs the python tests.
# Assumes that cs, sbt, pytest are all in your shell path.

# Make sure we can find sbt, cs, pipenv
hash sbt 2>/dev/null || { echo >&2 "Please install sbt first.  Aborting."; exit 1; }
hash pipenv 2>/dev/null || { echo >&2 "Please install pipenv first.  Aborting."; exit 1; }
hash cs 2>/dev/null || { echo >&2 "Please install cs first.  Aborting."; exit 1; }

# Note: Make sure version matches ones used in csw/LocationService.py and tests/testSupport/project/Libs.scala
#CSW_VERSION=4.0.0
CSW_VERSION=a9073713d8b5de90a817e08b31629a7176e1b4fe

logfile=test.log
set -x
cs launch csw-services:$CSW_VERSION -- start -e > $logfile 2>&1 &
cd tests/testSupport || exit 1
sbt clean stage  >> $logfile 2>&1
test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf   >> $logfile 2>&1 &
assemblyPid=$!
cd ../..
# give the background assembly time to initialize
sleep 10
# Run the python tests (add -s option to see stdout)
pipenv run python -m pytest tests
kill $assemblyPid
# Kill csw-services
kill `ps aux | grep 'csw-services' | grep -v grep | awk '{print $2}'`
