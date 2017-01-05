#!/bin/bash

n1=`wc -l /home/tian/Finn/log`
sleep 1
n2=`wc -l /home/tian/Finn/log`

while true; do
	if [ "$n1" == "$n2" ]; then
		echo "Start main.py ..." 
		python /home/tian/Finn/main.py $1 $2 || echo "Fail to run main.py !"
	fi
	sleep 61
done

