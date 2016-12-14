#!/usr/bin/python

import sys, getopt
import geoip2.database
import json

def lookupIP(ip):
    _db = "GeoLite2-City.mmdb"
    _ip = ip
    _format = "geojson" #["text", "geojson"]

    ## Search Database for IP ##

    reader = geoip2.database.Reader(_db)	# Load database
    try:
        res = reader.city(_ip)			# Query db for _ip
    except:
        return False
    else:
        coords = [res.location.longitude, res.location.latitude]	# Validate result coords then store
    
        if(_format == "text"):
            print coords
        if(_format == "geojson"):
            gjson = {"type": "Point", "coordinates": coords}
            print(json.dumps(gjson))

