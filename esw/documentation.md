## Introduction

This submodule contains python APIs for the [TMT Executive Software (ESW)](https://tmtsoftware.github.io/esw/),
including a Sequencer client and ESW Shell. 
See [here](https://tmtsoftware.github.io/esw/) for the ESW documentation.

You can find the [csw-python sources](https://github.com/tmtsoftware/csw-python) on GitHub.

Note that all APIs here assume that the latest version of CSW services are running 
For example, during development, run: `csw-services start`.

The Python APIs mirror the ESW Scala and Java APIs. The classes usually have the same fields,
with the difference that in some cases the Python types are simpler, due to less strict typing.

## ESW Shell

The esw-shell command provides an interactive shell with predefined imports
where you can type in CSW and ESW commands. The following example publishes an event:

```bash
> esw-shell.sh
Wellcome to ESW Shell
>>> source = Prefix(Subsystems.CSW, "testassembly")
>>> eventName = EventName("myAssemblyEvent")
>>> param = DoubleKey.make("assemblyEventValue").set(42.0)
>>> paramSet = [param]
>>> event = SystemEvent(source, eventName, paramSet)
>>> pub = EventPublisher()
>>> pub.publish(event)
>>> 
```

This is just an interactive Python session with the commonly used imports provided.
You can add your own imports, etc. The following example submits commands to an assembly:

```bash
> esw-shell.sh
Wellcome to ESW Shell
>>> prefix = Prefix(Subsystems.CSW, "TestClient")
>>> maybeObsId = []
>>> param = IntKey.make("testValue").set(42)
>>> paramSet = [param]
>>> cs = CommandService(Prefix(Subsystems.CSW, "TestPublisher"), ComponentType.Assembly)
>>> setup = Setup(prefix, CommandName("longRunningCommand"), maybeObsId, paramSet)
>>> resp = cs.submitAndWait(setup, 5)
>>> resp
Completed(runId='6c476544-4e84-4f8f-b10a-8172576ef68d', result=Result(paramSet=[]))
```

The `submitAndWait()` method submits a command and waits, if needed for the final response.
You can use plain `submit()` if the command returns a direct response.
There are also asynchronous versions of some methods: `queryFinalAsync()` and `submitAndWaitAsync()`,
that can be used in scripts using the `async` and `await` keywords.

```python
async def foo:
    resp1 = await cs.queryFinalAsync(runId, 5)
    resp2 = await cs.submitAndWaitAsync(setup, 5)
```

## ESW Sequencer Client

Assuming a sequencer is running, you can control it from Python using the ESW Sequencer Client (see [SequencerClient](SequencerClient.html)):

```python
from csw.Parameter import IntKey
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from esw.Sequence import Sequence
from esw.SequencerClient import SequencerClient
from esw.SequencerRes import Ok

sequencerPrefix = Prefix(Subsystems.ESW, "IRIS_ImagerOnly")
seqClient = SequencerClient(sequencerPrefix)
clientPrefix = Prefix(Subsystems.CSW, "TestClient")
maybeObsId = []
param = IntKey.make("testValue").set(42)
paramSet = [param]

def _makeSetup(name: str):
    return Setup(clientPrefix, CommandName(name), maybeObsId, paramSet)

setup1 = _makeSetup("Test1")
setup2 = _makeSetup("Test2")
setup3 = _makeSetup("Test3")
sequence = Sequence([setup1, setup2, setup3])
resp = seqClient.loadSequence(sequence)
assert (isinstance(resp, Ok))
```

See tests/esw/test_sequencer_client.py for some examples.
