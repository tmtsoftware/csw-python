# Releasing

* Check/update the tmtpycsw version in setup.py

* Check/update the CSW version in runTests.sh, test/testSupport/project/Libs.scala, runTest.sh, csw/LocationService.py.

* Run "make test" in top level dir
  (This starts a scala based backend and compares results with the python version).
 

* Run "make doc" in top level dir and check in the generated HTML docs
  (Note: Requires that pdoc3 is installed: To install, run: `pip3 install pdoc3`).

* Optional: Run "make release" in top level dir
  (Note: Requires username/password for pypi.org).

* Make GitHub release

