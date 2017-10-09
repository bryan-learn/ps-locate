#!/bin/bash
# only executes the command if it is the first week of the month
command="./update_geo_ip_db.sh"
day=$(date +%d)
if ((10#$day <= 7)) ; then
	exec $command
fi
exit 1
