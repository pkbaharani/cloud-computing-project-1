#!bin/bash
if [ "$#" = 0 ]
then
	echo " 2 positional Arguments required "
	exit 1
fi

sudo sh -c "echo 1 > /proc/sys/vm/drop_caches"
date
python3 surveillance.py $1 $2

