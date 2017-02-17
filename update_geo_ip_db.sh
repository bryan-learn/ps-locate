#!/bin/bash
echo "[$(date)] Begin GeoLite2 IP DB  update.."
cd ./geolocate
wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
gzip -d GeoLite2-City.mmdb.gz
if [ "$?" = "0" ]; then
	echo "[$(date)] update success"
else
	echo "[$(date)] update failed"
	exit 1
fi
