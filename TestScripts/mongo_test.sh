#!/bin/bash
i=1
if [ ! -e /local/repository/TestScripts/send.txt ]; then
  touch /local/repository/TestScripts/send.txt
fi

time (python ./mongo_test.py) >> /local/repository/TestScripts/send.txt 2>&1
