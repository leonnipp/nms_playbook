#!/bin/bash

PORT="1935"
URL="23.226.3.33"

COMMAND1=`sudo amp-tcpping -P "$PORT" -- "$URL"`
COMMAND2=`sudo amp-tcpping -P "$PORT" -- "$URL" | grep SYN`
# 0=Down
if [[ $(echo $COMMAND1) = *SYN* ]]; then
         TIME=`echo $COMMAND2 | awk '{print $3}'|awk -F "us" '{print $1}'`
         LOSS=0
 else
         TIME=0
         LOSS=100
fi

echo "tcpping,port=$PORT,url=$URL responsetime=$TIME,packet_loss=$LOSS"
