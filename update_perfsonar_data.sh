#!/bin/bash

# Using relative paths. Only run this script from root directory of the project (where it lives).

# download perfSONAR records
python ./ps_data/ps_data.py --download

# store perfSONAR records into local mongodb instance for 'staging'
python ./ps_data/ps_data.py --store

# process the 'staging' data to create geoip indexing
python ./geolocate/populate_ps_geoip.py

# copy 'staging' database to production database, 'ps-data'
python ./ps_data/ps_data.py --rotate

