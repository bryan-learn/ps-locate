#!/bin/bash
echo "[$(date)] Begin GeoLite2 IP DB  update.."
cd ./geolocate
wget -O new.mmdb.gz http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz > /dev/null 2>&1
if [ "$?" = "0" ]; then
	echo "[$(date)] download success"
else
	echo "[$(date)] download failed"
	exit 1
fi

gzip -d new.mmdb.gz
if [ "$?" = "0" ]; then
	echo "[$(date)] extraction success"
else
	echo "[$(date)] extraction failed"
	exit 1
fi

mv new.mmdb GeoLite2-City.mmdb
if [ "$?" = "0" ]; then
	echo "[$(date)] update success"
else
	echo "[$(date)] update failed"
	exit 1
fi
