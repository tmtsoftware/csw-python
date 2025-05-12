#!/bin/sh

test -d $HOME/.pyenv && exit 0
curl https://pyenv.run | bash
pyenv install -v 3.13.3
