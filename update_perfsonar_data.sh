#!/bin/bash

# Using relative paths. Only run this script from root directory of the project (where it lives).
echo "Begin perfSONAR DB update.."

cd ./ps_data
# download perfSONAR records
if python ./ps_data.py --download; then
	echo "    download: Success"
else
	echo "    download: Failed"
	exit 1
fi

# store perfSONAR records into local mongodb instance for 'staging'
if python ./ps_data.py --store; then
	echo "    store: Success"
else
	echo "    store: Failed"
	exit 1
fi

cd ../geolocate
# process the 'staging' data to create geoip indexing
if python ./populate_ps_geoip.py; then
	echo "    geoip indexing: Success"
else
	echo "    geoip indexing: Failed"
	exit 1
fi

cd ../ps_data
# copy 'staging' database to production database, 'ps-data'
if python ./ps_data.py --rotate; then
	echo "    rotate: Success"
else
	echo "    rotate: Failed"
	exit 1
fi

echo "perfSONAR DB update: Success"

