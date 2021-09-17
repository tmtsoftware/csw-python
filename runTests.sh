#!/bin/bash

# Script that starts the CSW services, compiles and runs the test assembly and then runs the python tests.
# Assumes that cs, sbt, pytest are all in your shell path.

CSW_VERSION=4.0.0-RC2
#CSW_VERSION=87d677d5ad39b6781619f1f866c90ee6ec448c5b

logfile=test.log
if ! hash cs 2>/dev/null ; then
    echo >&2 "Please install coursier (https://get-coursier.io/).  Aborting."
    exit 1
fi
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
