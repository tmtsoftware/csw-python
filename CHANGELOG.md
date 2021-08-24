# Change Log
All notable changes to this project will be documented in this file.

## [tmtpycsw v4.0.0] - 2021-08-24

### Changed

- Updated for CSW-4.0.0-RC1

- Removed CSW `struct` parameter type

- Published to https://pypi.org/project/tmtpycsw/4.0.0/

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

    