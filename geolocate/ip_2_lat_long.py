#!/usr/bin/python

import sys, getopt
import geoip2.database
import json

def main(argv):
    ## Process CLI Args ##
    _db = "GeoLite2-City.mmdb"
    _ip = None
    _format = "text" #["text", "geojson"]

    try:
       opts, args = getopt.getopt(argv,"hi:d:f:",["ip=","db=","format="])
    except getopt.GetoptError:
       print 'ip_2_lat_long.py -i <IP Address> -d <dbfile>'
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'ip_2_lat_long.py -i <IP Address> -d <dbfile>'
            sys.exit()
        elif opt in ("-i", "--ip"):
            _ip = arg
        elif opt in ("-d", "--db"):
            _db = arg
        elif opt in ("-f", "--format"):
            _format = arg

    if(_ip is None):
        print 'Required argument missing: An IP address is required.'
        print 'ip_2_lat_long.py -i <IP Address> -d <dbfile>'
        sys.exit(2)

    ## Search Database for IP ##

    reader = geoip2.database.Reader(_db) 			# Load database
    try:
        res = reader.city(_ip)					# Query db for _ip
    except:
        print "No address found for IP Address:", _ip
    else:
        coords = [res.location.longitude, res.location.latitude]	# Validate result coords then store
    
        if(_format == "text"):
            print coords
        if(_format == "geojson"):
            gjson = {"type": "Point", "coordinates": coords}
            print(json.dumps(gjson))

if __name__ == "__main__":
    main(sys.argv[1:])

