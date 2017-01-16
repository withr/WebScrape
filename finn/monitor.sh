#!/bin/bash

if [ $# == 0 ]; then
    echo "Monitor all crawlers: "
    while true; do
        # msg=`wc -l log_? |sed '$d' | tr '\n' ';        '` 
        msg=`wc -l log_?  | tr '\n' '; '`
        echo -ne "$msg"\\r
        sleep 1
    done
else
    echo "Monitor disk usages:"
    while true; do
        msg=`du -s pages_? | tr '\n' '; '`
        # msg=`du -s pages_$1 | tr '\n' ' '`
        echo -ne "$msg"\\r
        sleep 10
    done    
fi

