#!/usr/bin/python

import sys, getopt
import logging
import pymongo
import ip2geo
import json

def main(argv):
    ## Config Log ##
    logging.basicConfig(filename='log/ps-locate.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

    ## Process CLI Args ##
    _ip = None
    config = {
        'db-url': "mongodb://localhost",
        'db-port': 27017,
        'db-name': "staging",
        'host-count': 3
    }


    try:
       opts, args = getopt.getopt(argv,"hi:u:p:d:c:",["ip=","url=","port=","db=","count="])
    except getopt.GetoptError:
       print 'ps-locate.py -i <IP Address> -u <db url> -p <port> -d <db name>'
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'ps-locate.py -i <IP Address> -u <db url> -p <port> -d <db name>'
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
            config['host-count'] = arg

    if(_ip is None):
        print 'Required argument missing: An IP address is required.'
        print 'ps-locate.py -i <IP Address> -u <db url> -p <port> -d <db name>'
        sys.exit(2)

    ## Get coordinates of incoming IP ##
    try:
        coords = ip2geo.lookupIP(_ip, _format="geojson")
    except:
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
    cursor = db.geodata.aggregate([	# query db for nearest hosts
        {$geoNear:{			# get list of coordinates sorted by shortest distance
            near: coords,
            distanceField: "distance",
            spherical: true
        }},
        {$group:{_id: "$_id", minDist: {$min: "$distance"}}},	# group by host, storing minimun distance per host
        {$limit: config['host-count']},				# only return 'host-count' number of hosts
        {$lookup: {from: "correlated", localField:"_id", foreignField:"_id", as:"keys"}},	# left outer join on 'correlated' collection to get keys
        {$project: {_id:"$_id", interfaces: "$keys.interfaces", addresses:"$keys.addresses"}},	# project fields to get desired format
        {$unwind: "$interfaces"},				# these unwinds are needed because we have nested arrays
        {$unwind: "$addresses"},				# TODO look into how to prevent nesting arrays during data population
        {$unwind: "$addresses"},
        {$unwind: "$addresses"}
    ])

    ## Query related data for target hosts ##
    interfaceCursor = None
    serviceCursor = None
    hostCursor = None
    fullHostRecords = []
    for document in cursor:
        interfaceCursor = db.interfaces.find({		# query for linked interface records (1+)
            "uri": {"$in": document['interfaces']}
        })

        serviceCursor = db.services.find({		# query for linked service records (1+)
            "service-host": document['_id']
        })

        hostCursor = db.hosts.find({			# query for linked host record (1)
            "uri": document['_id']
        })

        # check for errors

        # build complete host record with all data
        fullHost = dict(host=hostCursor.next())

    ## Output results in json format ## (human and machine readible interface)
    
    
def connectToMongodb():
    # config mongodb connection and database to use
    url = config['db-url'] +":"+ str(config['db-port'])
    client = pymongo.MongoClient(url)
    return client


if __name__ == "__main__":
    main(sys.argv[1:])

