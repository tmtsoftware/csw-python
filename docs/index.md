# Python APIs for CSW and ESW

This repository contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw)
and [TMT Executive Software (ESW)](https://tmtsoftware.github.io/esw/).

* [Python APIs for CSW](csw/index.html)
* [Python APIs for ESW](esw/index.html)

## Requirements

* Python version 3.13
* pdoc3 (`pip3 install pdoc3`)
* pipenv (latest)

### Python Dependencies:

The Python dependencies can be installed in a local "virtual environment"
by typing:

```
make venv
```

This uses pip and pipenv to create a .venv directory containing the dependencies and python interpreter.
Then you can activate the virtual environment by sourcing one of the .venv/bin/activate* scripts.

```bash
$ . .venv/bin/activate
```

The latest releases are published to https://pypi.org/project/tmtpycsw/ and can be installed with:

    pip3 install tmtpycsw


