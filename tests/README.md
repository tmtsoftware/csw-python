# Running the Tests

A Makefile and script are provided to run the tests.
Typing `make test` in the top level csw-python directory checks that the virtual environment (in .venv) exists
and then runs: `runTests.sh` to set up the test environment and run the tests.

This assumes that [cs](https://get-coursier.io/) (used to start the correct version of csw-services), 
sbt and pytest are in your shell path and that all the required python packages are installed. See [here](https://tmtsoftware.github.io/csw/apps/cswservices.html) for 
how to install csw-services.

Alternatively, to manually run the tests: 

Create the Python virtual environment (Do this once, or after dependencies change):

    make venv

start the CSW services:

    csw-services start

Then compile and start the test assembly:

    cd tests/testSupport
    sbt stage
    test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf

Then, to run the tests, run:

    . .venv/bin/activate
    pytest

from the top level csw-python directory. Afterwards, kill the assembly and csw-services with Ctrl-C.

