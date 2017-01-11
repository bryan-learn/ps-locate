#!/usr/bin/python

import sys, getopt, os
import logging
import geoip2.database
import json

def lookupIP(_ip, _dbPath="./", _db="GeoLite2-City.mmdb", _format="geojson"):
    ## Search Database for IP ##
    fullPath = _dbPath+_db

    reader = geoip2.database.Reader(fullPath)	# Load database
    try:
        res = reader.city(_ip)			# Query db for _ip
    except (SystemExit, KeyboardInterrupt):
        raise					# Do not consume these exceptions, but consume any others
    except:
        logging.warning('No match found for lookup on "{0}"'.format(_ip))
        return False				# Return False if lookup raised any other exception
    else:
        coords = [res.location.longitude, res.location.latitude]	# Validate result coords then store
    
        if(_format == "text"):
            return coords
        if(_format == "geojson"):
            gjson = {"type": "Point", "coordinates": coords}
            return gjson

