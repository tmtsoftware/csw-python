# Running the Tests

Before running the tests, start the CSW services:

    csw-services.sh start

Then compile and start the test assembly:

    cd testSupport
    sbt stage
    test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf

Then, to run the tests, run:

    pytest

in this directory. Afterwards, kill the assembly with Ctrl-C and stop the CSW services with:

    csw-services.sh stop

