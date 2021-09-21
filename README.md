# tmtpycsw - Python3 CSW APIs

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw). 

Note: Python version 3.9 was used for testing.

The latest release has been published to https://pypi.org/project/tmtpycsw/ and can be installed with:

    pip3 install tmtpycsw

See [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
for how to set up a local Python environment with the necessary dependencies for testing
this project.

## API Documentation

See [here](https://tmtsoftware.github.io/pycsw/index.html) for an overview of this package and the 
generated API documentation.

Run `make doc` to generate the user manual and API documentation for the Python classes. 
Then open `build/csw/index.html`. 
(Note: Requires that pdoc is installed: To install, run: `pip install pdoc`.)

## Running the tests

You can run the tests by typing `make test`.
This creates the .venv directory, if it does not exist, and then runs the `runTests.sh` script,
which does some checks and then uses pytest to run the tests.

Some of the tests require that csw-services and a Scala based CSW command service application are running in the background.
These are started in the runTests.sh script. 
Once they are running, you can run all the tests with:
```
pipenv run python -m pytest tests
```
