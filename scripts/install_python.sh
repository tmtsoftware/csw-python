#!/bin/sh

sudo apt install -y build-essential libssl-dev zlib1g-dev libsqlite3-dev libffi-dev

#test -d $HOME/.pyenv && exit 0
#curl https://pyenv.run | bash
pyenv install -v 3.13.3
