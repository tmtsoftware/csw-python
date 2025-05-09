#!/bin/sh

CSW_VERSION=6.0.0
CS_CHANNEL="https://raw.githubusercontent.com/tmtsoftware/osw-apps/branch-6.0.x/apps.json"
cs launch --channel $CS_CHANNEL csw-services:$CSW_VERSION -- start -e -c -k
