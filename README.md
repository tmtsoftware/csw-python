# Python CSW APIs

This package contains Python APIs for [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw)
and [TMT Executive Software (ESW)](https://tmtsoftware.github.io/esw/). 

Note: Python version 3.13 was used for testing.

The latest releases are published to https://pypi.org/project/tmtpycsw/ and can be installed with:

    pip3 install tmtpycsw

See [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
for how to set up a local Python environment with the necessary dependencies for testing
this project.

## Version compatibility

| csw-python | csw    |
|------------|--------|
| v6.0.0     | v6.0.0 |
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

## CSW and ESW APIs

Many of the CSW and ESW classes have Python versions here.
The following CSW service APIs are supported in Python:

* Config Service
* Event Service
* Command Service (server and client)
* Location Service
* Time Service

The Alarm Service is not yet implemented in Python.

See the test cases for examples of using the services.
Note that some of the tests require that the csw-services have been started.

## Sequencer Scripts

The [sequencer/examples/testData](sequencer/examples/testData) directory contains some
example sequencer scripts written in Python. These scripts are used in some of the esw
integration test cases when the `enableEswPythonScripting` system property is set to true (`-DenableEswPythonScripting=true`) in esw.
The current implementation also requires two environment variables to be set before running the Python based esw script server 
[sequencer/OcsScriptServer.py](sequencer/OcsScriptServer.py):

* CSW_PYTHON - should be set to the directory containing this README.md file
* PYTHONPATH - should be set to the same value as CSW_PYTHON (used by Python to find dependencies)

The script server application is started automatically by esw when needed. 
An HTTP client on the esw side communicates with the script server.

# Python Syntax for Sequencer Scripts

Since Python does not allow passing code blocks as parameters (as is done in the Kotlin DSL version), 
the syntax for esw Python sequencer scripts uses *decorations* (like Java annotations).

In Kotlin, sequencer scripts start with:

    script {

In Python, you define a function called `script` that takes a context argument of type Script:

```aiignore
    def script(ctx: Script):
```

The ctx parameter of type Script class contains the APIs needed by the script.
The Kotlin version handles Setups like this:

```aiignore
    onSetup("command-4") {
        val setupCommand = Setup("ESW.test", "command-3")
        val sequence = sequenceOf(setupCommand)
        val tcsSequencer = Sequencer(TCS, ObsMode("darknight"), 10.seconds)
        tcsSequencer.submitAndWait(sequence, 10.seconds)
    }
```

In Python, decorators are used, for example:

```aiignore
    @ctx.onSetup("command-4")
    async def handleCommand4(_: Setup):
        setupCommand = ctx.Setup("ESW.test", "command-3")
        sequence = ctx.sequenceOf(setupCommand)
        tcsSequencer = ctx.Sequencer(Subsystem.TCS, ObsMode("darknight"))
        await tcsSequencer.submitAndWait(sequence, timedelta(seconds=10))
```

Note that the Python sequencer scripts are asynchronous (using async/await), so you need to `await` any 
calls to async functions.

Scheduling tasks in the Kotlin sequencer scripts looks like this:

```aiignore
    onSetup("schedule-periodically-from-now") {
        val currentTime = utcTimeNow()
        var counter = 0
        val a = schedulePeriodicallyFromNow(1.seconds, 1.seconds) {
            val param = longKey("offset").set(currentTime.offsetFromNow().absoluteValue.inWholeMilliseconds)
            publishEvent(SystemEvent("ESW.schedule.periodically", "offset", param))
            counter += 1
        }
        loop {
            stopWhen(counter > 1)
        }
        a.cancel()
    }
```

The same can be done in the Python version:

```aiignore
    @ctx.onSetup("schedule-periodically-from-now")
    async def handleSchedulePeriodicallyFromNow(_: Setup):
        currentTime = ctx.utcTimeNow()
        counter = 0

        async def publishEvents():
            nonlocal counter
            param = longKey("offset").set(round(abs(currentTime.offsetFromNow().total_seconds() * 1000)))
            await ctx.publishEvent(ctx.SystemEvent("ESW.schedule.periodically", "offset", param))
            counter = counter + 1

        a = ctx.schedulePeriodicallyFromNow(timedelta(seconds=1), timedelta(seconds=1), publishEvents)

        async def countEvents():
            ctx.stopWhen(counter > 1)

        await ctx.loop(countEvents, milliseconds=50)

        a.cancel()
```

Note that the Python version uses nested functions, since you can't pass code blocks as parameters (as is done in the Kotlin version).
Compare the example sequencer scripts under [sequencer/examples](sequencer/examples) with the ones in esw/examples 
to see further differences.

