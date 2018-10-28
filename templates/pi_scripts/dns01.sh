#!/bin/bash

PORT="53"
URL="10.15.22.16"

COMMAND1=`sudo amp-tcpping -P "$PORT" -- "$URL"`
COMMAND2=`sudo amp-tcpping -P "$PORT" -- "$URL" | grep SYN`
# 0=Down
if [[ $(echo $COMMAND1) = *SYN* ]]; then
         TIME=`echo $COMMAND2 | awk '{print $3}'|awk -F "us" '{print $1}'`
 else
         TIME=0
fi

echo "tcpping,port=$PORT,url=$URL responsetime=$TIME"
