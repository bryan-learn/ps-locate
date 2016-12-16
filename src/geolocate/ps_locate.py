#!/usr/bin/python

import sys, getopt
import logging
import pymongo
import ip2geo
import json
from bson import json_util

config = {
    'db-url': "mongodb://localhost",
    'db-port': 27017,
    'db-name': "staging",
    'host-count': 3,
    'outfile': None
}

def main(argv):
    ## Config Log ##
    logging.basicConfig(filename='log/ps-locate.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

    ## Process CLI Args ##
    _ip = None

    syntaxStr = 'ps-locate.py -i <IP Address> [-u <db url>] [-p <port>] [-d <db name>] [-c <host count>] [-o <output file>]'

    try:
       opts, args = getopt.getopt(argv,"hi:u:p:d:c:o:",["ip=","url=","port=","db=","count=", "outfile="])
    except getopt.GetoptError:
       print syntaxStr
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print syntaxStr
            print "If no outfile is provided, result will printed to output stream"
            sys.exit()
        elif opt in ("-i", "--ip"):
            _ip = arg
        elif opt in ("-u", "--db"):
            config['db-url'] = arg
        elif opt in ("-p", "--port"):
            config['db-port'] = arg
        elif opt in ("-d", "--db"):
            config['db-name'] = arg
        elif opt in ("-c", "--count"):
            config['host-count'] = int(arg)
        elif opt in ("-o", "--outfile"):
            config['outfile'] = arg

    if(_ip is None):
        print 'Required argument missing: An IP address is required.'
        print syntaxStr
        sys.exit(2)

    ## Get coordinates of incoming IP ##
    coords = ip2geo.lookupIP(_ip, _format="geojson")
    if(not coords):
        logging.warning("Unable to get coordinates for provided IP '{0}'".format(_ip))
        sys.exit(2)

    ## Query MongoDB for nearest hosts ##
    '''
    Returns N='host-count' records in the format:
    {
	"_id": "lookup/host/9347f521-cb68-4376-879b-c3677974ebb4",
	"interfaces": ["lookup/interface/6ba46879-c3ad-4e22-8864-1a6ad059eda1"],
	"addresses": ["192.80.83.53"]
    }
    '''
    dbClient = connectToMongodb()	# connect to database using config
    db = dbClient[config['db-name']]
    nearbyHostsCursor = db.geodata.aggregate([	# query db for nearest hosts
        {"$geoNear":{			# get list of coordinates sorted by shortest distance
            "near": coords,
            "distanceField": "distance",
            "spherical": "true"
        }},
        {"$group":{"_id": "$_id", "minDist": {"$min": "$distance"}}},	# group by host, storing minimun distance per host
        {"$limit": config['host-count']},				# only return 'host-count' number of hosts
        {"$lookup": {"from": "correlated", "localField":"_id", "foreignField":"_id", "as":"keys"}},	# left outer join on 'correlated' collection to get keys
        {"$project": {"_id":"$_id", "interfaces": "$keys.interfaces", "addresses":"$keys.addresses"}},	# project fields to get desired format
        {"$unwind": "$interfaces"},				# these unwinds are needed because we have nested arrays
        {"$unwind": "$addresses"},				# TODO look into how to prevent nesting arrays during data population
        {"$unwind": "$addresses"},
        {"$unwind": "$addresses"}
    ])

    ## Query related data for target hosts ##
    interfaceCursor = None
    serviceCursor = None
    hostCursor = None
    fullHostRecords = []

    for document in nearbyHostsCursor:
#        # convert document values from unicode to string type (I think the query fails when values are submitted as unicode)
#        for iface in document['interfaces']:
#            iface = str(iface)
#        document['_id'] = str(document['_id'])
#

        interfaceCursor = db.interfaces.find({		# query for interface records linked to this host (1+)
            "uri": {"$in": document['interfaces']}
        })

        serviceCursor = db.services.find({		# query for service records linked to this host (1+)
            "service-host": document['_id']
        })

        hostCursor = db.hosts.find({			# query for host record linked to this host (1)
            "uri": document['_id']
        })

        # check for errors
        if(interfaceCursor.alive and serviceCursor.alive and hostCursor.alive):	# TODO find better test than .alive - doesn't always mean cursor.next() will succeed.
            # build complete host record with all data
            fullHost = dict(host={}, interfaces=[], services=[])
            fullHost['host'] = hostCursor.next()		# add host record to fullHost
            for serv in serviceCursor:				# add service records to fullHost
                fullHost['services'].append(serv)
            for iface in interfaceCursor:			# add interface records to fullHost
                fullHost['interfaces'].append(iface)
    
            fullHostRecords.append(fullHost)			# append fullHost record to final list 
        else:
            print "Query failed. Host: {0}, Services: {1}, Interfaces: {2}".format(interfaceCursor.alive, serviceCursor.alive, hostCursor.alive)


    ## Output results in json format ## (human and machine readible interface)
    json_records = json.dumps(fullHostRecords, default=json_util.default)	# encode as json

    if(config['outfile'] is not None):			# if outfile provide, write to file
        with open(config['outfile'], 'w') as fp:
            fp.write(str(json_records))
    else:						# otherwise print to output stream
        print(str(json_records))

 
def connectToMongodb():
    # config mongodb connection and database to use
    url = config['db-url'] +":"+ str(config['db-port'])
    client = pymongo.MongoClient(url)
    return client


if __name__ == "__main__":
    a=main(sys.argv[1:])

