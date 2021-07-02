# Running the Tests

A script is provided to run the tests:

    runTest.sh

This assumes that csw-services (version 4.0.0-M1), sbt and pytest are in your shell path and that all the required python packages are installed. See [here](https://tmtsoftware.github.io/csw/apps/cswservices.html) for 
how to install csw-services.

Alternatively, to manually run the tests: start the CSW services:

    csw-services start

Then compile and start the test assembly:

    cd testSupport
    sbt stage
    test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf

Then, to run the tests, run:

    pytest

in this directory. Afterwards, kill the assembly and csw-services with Ctrl-C.

