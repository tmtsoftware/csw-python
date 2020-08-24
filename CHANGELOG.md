# Change Log
All notable changes to this project will be documented in this file.

## [tmtpycsw vXXX] - 2020-XXX

### Changed

- Updated for latest csw version

- Changed event service code to get the redis sentinel location from the location service and use it (previously used hard coded host:port)

- Added unsubscribe method to EventSubscriber (Used to unsubscribe only: You can also call stop() on the event subscriber thread returned from the subscribe call to stop the listening thread.)

- Added pSubscribe() and pUnsubscribe() methods to EventSubscriber (matching the CSW versions) for subscribing to an event key pattern

## [tmtpycsw v2.0.1] - 2020-05-15

### Added

- Added documentation, test code

### Changed

- Updated for csw-2.0.1

    