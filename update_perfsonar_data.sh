#!/bin/bash

# Using relative paths. Only run this script from root directory of the project (where it lives).
echo "[$(date)] Begin perfSONAR DB update.."

cd ./ps_data
# download perfSONAR records [attempt 3 times]
if python ./ps_data.py --download; then
	echo "    [$(date)] download: Success"
else
	echo "    [$(date)] download: Failed (try 1)"
	sleep 30
	if python ./ps_data.py --download; then
		echo "    [$(date)] download: Success"
	else
		echo "    [$(date)] download: Failed (try 2)"
		sleep 30
		if python ./ps_data.py --download; then
			echo "    [$(date)] download: Success"
		else
			echo "    [$(date)] download: Failed (try 3)"
			exit 1
		fi
	fi
fi

# store perfSONAR records into local mongodb instance for 'staging'
if python ./ps_data.py --store; then
	echo "    [$(date)] store: Success"
else
	echo "    [$(date)] store: Failed"
	exit 1
fi

cd ../geolocate
# process the 'staging' data to create geoip indexing
if python ./populate_ps_geoip.py; then
	echo "    [$(date)] geoip indexing: Success"
else
	echo "    [$(date)] geoip indexing: Failed"
	exit 1
fi

cd ../ps_data
# copy 'staging' database to production database, 'ps-data'
if python ./ps_data.py --rotate; then
	echo "    [$(date)] rotate: Success"
else
	echo "    [$(date)] rotate: Failed"
	exit 1
fi

echo "[$(date)] perfSONAR DB update: Success"

