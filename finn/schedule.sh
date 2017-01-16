#!/bin/bash

n1=`wc -l /home/tian/HDD1T/Finn/log_$1`
sleep 5
n2=`wc -l /home/tian/HDD1T/Finn/log_$1`

if [ "$n1" == "$n2" ]; then
    python /home/tian/HDD1T/Finn/crawler.py $1
    echo "Start crawler.py $1"
fi


