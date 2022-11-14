# Python CSW APIs

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw)
and the [TMT Executive Software (ESW)](https://tmtsoftware.github.io/esw/). 

Note: Python version 3.10 was used for testing.

The latest release has been published to https://pypi.org/project/tmtpycsw/ and can be installed with:

    pip3 install tmtpycsw

See [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
for how to set up a local Python environment with the necessary dependencies for testing
this project.

## Version compatibility

| csw-python | csw    |
|------------|--------|
| v5.0.0     | v5.0.0 |
| v4.0.3     | v4.0.1 |
| v4.0.2     | v4.0.1 |
| v4.0.1     | v4.0.0 |
| v4.0.0     | v4.0.0-RC1 |
| v3.0.6     | v3.0.1 |
| v3.0.5     | v3.0.0 |
| v3.0.4     | v3.0.0-RC1 |
| v3.0.3     | v3.0.0-M1 |
| v3.0.2     | v3.0.0-M1 |
| v2.0.1     | v2.0.1 |
| v2.0.0     | v2.0.0 |


## API Documentation

See [here](https://tmtsoftware.github.io/csw-python/index.html) for an overview of this package and the 
generated API documentation.

Run `make doc` to generate the user manual and API documentation for the Python classes. 
Then open `build/csw/index.html`. 
(Note: Requires that pdoc3 is installed: To install, run: `pip3 install pdoc3`.)

## Running the tests

You can run the tests by typing `make test`.
This creates the .venv directory, if it does not exist, and then runs the `runTests.sh` script,
which does some checks and then uses pytest to run the tests.
