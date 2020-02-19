#!/bin/bash

# Script that starts the CSW services, compiles and runs the test assembly and then runs the python tests.
# Assumes that csw-services.sh, sbt, pytest are all in your shell path.

set -v
csw-services.sh start
cd testSupport
sbt stage
test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf &
assemblyPid=$!
cd ..
# give the background assembly time to initialize
sleep 5
# Run the python tests
pytest
kill $assemblyPid
csw-services.sh stop
