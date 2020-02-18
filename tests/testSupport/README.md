# test

This project implements an HCD (Hardware Control Daemon) and an Assembly using 
TMT Common Software ([CSW](https://github.com/tmtsoftware/csw)) APIs. 

## Subprojects

* test-assembly - an assembly that talks to the test HCD
* test-hcd - an HCD that talks to the test hardware
* test-deploy - for starting/deploying HCDs and assemblies

## Build Instructions

The build is based on sbt and depends on libraries generated from the 
[csw](https://github.com/tmtsoftware/csw) project.

See [here](https://www.scala-sbt.org/1.0/docs/Setup.html) for instructions on installing sbt.

## Prerequisites for running Components

The CSW services need to be running before starting the components. 
This is done by starting the `csw-services.sh` script, which is installed as part of the csw build.
If you are not building csw from the sources, you can get the script as follows:

 - Download csw-apps zip from https://github.com/tmtsoftware/csw/releases.
 - Unzip the downloaded zip.
 - Go to the bin directory where you will find `csw-services.sh` script.
 - Run `./csw_services.sh --help` to get more information.
 - Run `./csw_services.sh start` to start the location service and config server.

## Building the HCD and Assembly Applications

 - Run `sbt test-deploy/universal:packageBin`, this will create self contained zip in `test-deploy/target/universal` directory
 - Unzip the generated zip and cd into the bin directory

Note: An alternative method is to run `sbt stage`, which installs the applications locally in `test-deploy/target/universal/stage/bin`.

## Running the HCD and Assembly

Run the container cmd script with arguments. For example:

* Run the HCD in standalone mode with a local config file (The standalone config format is differennt than the container format):

```
./target/universal/stage/bin/test-container-cmd-app --standalone --local ./src/main/resources/SampleHcdStandalone.conf
```

* Start the HCD and assembly in a container using the Java implementations:

```
./target/universal/stage/bin/test-container-cmd-app --local ./src/main/resources/JSampleContainer.conf
```

* Or the Scala versions:

```
./target/universal/stage/bin/test-container-cmd-app --local ./src/main/resources/SampleContainer.conf
```
