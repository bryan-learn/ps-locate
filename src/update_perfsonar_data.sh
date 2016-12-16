#!/bin/bash

# Using relative paths. Only run this script from src/ directory of project (where it lives).

cd ./ps-data
# download perfSONAR records from simple_lookup_service
python download_all_records.py

# store perfSONAR records in local mongoDB
python load_records_to_mongo.py

cd ../geolocate
# lookup the geo coordinates for all available IP addresses in perfSONAR data
python populate_ps_geoip.py

cd ../ps-data
# Previous steps updated the 'staging' database. Now we can remove old data and rotate 'staging' to 'ps-data'
python rotate_dbs.py
