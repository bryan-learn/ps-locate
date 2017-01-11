#!/usr/bin/python

import sys, getopt
import logging
import geoip2.database
import json
import ip2geo

def main(argv):
    ## Config Log ##
    logging.basicConfig(filename='log/cli_ip2geo.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

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
    logging.debug("lookup {0} in {1} with format {2}".format(_ip, _db, _format))
    ip2geo.lookupIP(_ip, _db, _format)

if __name__ == "__main__":
    main(sys.argv[1:])

