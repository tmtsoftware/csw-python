#!/bin/sh

export PYTHONPATH=`pwd`

# Starts an interactive Python shell with CSW and ESW imports predefined
. .venv/bin/activate
python -i esw/esw-shell.py
