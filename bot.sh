#!/bin/bash
source ./dict-env/bin/activate
# "$@" passes all terminal arguments to the python script
python ./bot.py "$@"