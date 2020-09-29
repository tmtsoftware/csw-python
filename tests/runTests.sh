#!/bin/bash

# Script that starts the CSW services, compiles and runs the test assembly and then runs the python tests.
# Assumes that csw-services.sh, sbt, pytest are all in your shell path.

logfile=test.log
set -v
#csw-services.sh --version v3.0.0-M1 start -e > $logfile 2>&1 &
csw-services.sh start -e > $logfile 2>&1 &
cd testSupport || exit 1
sbt clean stage  >> $logfile 2>&1
test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf   >> $logfile 2>&1 &
assemblyPid=$!
cd ..
# give the background assembly time to initialize
sleep 10
# Run the python tests
pytest --capture=tee-sys
kill $assemblyPid
csw-services.sh stop  >> $logfile 2>&1
