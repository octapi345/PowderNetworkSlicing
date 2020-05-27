#!/bin/bash

# Run appropriate setup script

NODE_ID=$(geni-get client_id)

if [ $NODE_ID = "rue1" ]; then
    /local/repository/bin/start-ue.sh
elif [ $NODE_ID = "enb1" ]; then
    /local/repository/bin/start-enb.sh
else
    echo "no setup necessary"
fi
