# Change Log
All notable changes to this project will be documented in this file.

## [tmtpycsw v4.0.4] - 

### Changed

- Updated dependencies and moved to Python 3.10
- Changed the way parameters are accessed to be more like the Java/Scala CSW APIs
- Added use of Python Generics for keys and parameters, to provide type hints for IDEs
- Added Sequencer client APIs (so you can control a running sequencer from Python)
- Add an esw-shell application, similar to the Scala CSW one (see ./esw-shell.sh wrapper)
- Added command service client features (class csw.CommandService)
- Renamed KeyType enum to KeyTypes and added KeyType class hierarchy, similar to CSW APIs
- Refactored code to use new python 3.10 features
- Added code to find a unique port when registering with the Location Service with port=0
- Updated Units to match latest CSW version
- Fixed issue with Redis sentinal (need to use localhost)
- Updated CSW version to SHA of the latest snapshot
- Added Command Service and Config Service client APIs

## [tmtpycsw v4.0.3] - 2022-04-27

### Changed

- Minor changes to Makefile
- Changed to use pdoc3 instead of pdoc
- Removed outdated dependency on pathlib
- Checked in test data file that was missing
- Updated Pipfile.lock
- Changed Makefile to define PYTHON as python3.9 (override with make PYTHON=python3.x if needed)

## [tmtpycsw v4.0.2] - 2022-02-14

### Changed

- Updated for csw-4.0.1
- Updated dependencies

## [tmtpycsw v4.0.1] - 2021-09-27

### Changed

- Renamed GitHub repo from pycsw to csw-python (The pypi package is still named "tmtpycsw")
- Changed type of "prefix" arguments from str to Prefix, matching CSW API
- Changed type of event name arguments to EventName and command name to ComandName, in line with the CSW API
- Updated Location Service Registration classes to more closely match CSW APIs
- Updated code to handle different time value formats in JSON and CBOR encodings of parameter values
- Added tests
- Updated for CSW-4.0.0

### Added

- Added EventKey class and used it instead of str for event keys
- Adding logging support (use: `log = structlog.get_logger()`)
- Added enums for KeyType, Subsystem, Units
- Added missing ComponentType values (SequenceComponent, Machine) and changed case to match CSW API
- Added ComponentId class and additional constructor for ConnectionInfo
- Added tests, updated existing examples and tests

## [tmtpycsw v4.0.0rc1] - 2021-08-24

### Changed

- Updated for CSW-4.0.0-RC1

- Removed CSW `struct` parameter type

- Published to https://pypi.org/project/tmtpycsw/4.0.0rc1/

## [tmtpycsw v3.0.6] - 2020-12-01

### Changed

- Updated for CSW-3.0.1

- Added code to unsubscribe current state subscribers on web socket close

## [tmtpycsw v3.0.4] - 2020-12-01

### Changed

- Updated for CSW-3.0.0-M1 and change in NetworkType JSON encoding

## [tmtpycsw v3.0.3] - 2020-10-14

### Added

- Added Command Service test

### Changed

- Updated dependencies

## [tmtpycsw v3.0.2] - 2020-10-12

### Changed

- Fixed issue with "Current State" publishing from python code.

## [tmtpycsw v3.0.1] - 2020-09-29

### Changed

- Updated for latest csw version (v3.0.0-M1)

- Changed event service code to get the redis sentinel location from the location service and use it (previously used hard coded host:port)

- Added unsubscribe method to EventSubscriber (Used to unsubscribe only: You can also call stop() on the event subscriber thread returned from the subscribe call to stop the listening thread.)

## [tmtpycsw v2.0.1] - 2020-05-15

### Added

- Added documentation, test code

### Changed

- Updated for csw-2.0.1

    