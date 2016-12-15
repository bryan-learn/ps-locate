'''
Queries Mongo for list of all IP addresses in the interface records.
Looks up coordinates for each IP address then inserts the geojson format into 'geodata' collection.
Example geodata record:
{
    "location": {"type": "Point", "coordinates": [180, 90]},
    "_id": "<host-uri>"
}
'''

#from memory_profiler import profile
import logging
import pymongo
import json
import re
import ip2geo

logging.basicConfig(filename='log/populate_ps_geoip.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

config = {
    'db-url': "mongodb://localhost",
    'db-port': 27017,
    'db-name': "staging"
}

def connectToMongodb():
    # config mongodb connection and database to use
    url = config['db-url'] +":"+ str(config['db-port'])
    client = pymongo.MongoClient(url)
    return client

def indexConfig(db):
    db['geodata'].create_index([
        ("location", pymongo.GEOSPHERE)		# create 2dSphere index on the field "location"
    ])
    
#@profile
def store2Mongo(db, collectionStr, records):
    # use collection from collectionStr; creates collection if doesn't exist
    coll = db[collectionStr]
    result = coll.insert_many(records)
    
    return result

## Setup new Mongo DB collection ##
dbClient = connectToMongodb()			# connect to local mongo db
indexConfig(dbClient[config['db-name']])	# create 'geodata' collection and add index to it

## Query for list of IPs ##
db = dbClient[config['db-name']]
cursor = db.correlated.find({},{"addresses": 1, "_id": 1})	# query all records from "correlated" collection. Only get fields "addresses" and "_id"

## Look up coordinates for each IP address ##

#regex pattern for IPv6 addresses
ipv6_pattern = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"

#regex pattern for IPv4 addresses
ipv4_pattern = "((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"

## Build geodata records ##
'''
Example geodata record:
{
    "location": {"type": "Point", "coordinates": [180, 90]},
    "_id": <host-uri>
}
'''
geoList = []
for document in cursor:				# Create a geojson object per address for "location" field of record
    aRec = None
    ipList = document['addresses'][0]
    for ip in ipList:				# validate each IP address
        ip = str(ip[0])
        v4_match = re.match( ipv4_pattern, ip)
        v6_match = re.match( ipv6_pattern, ip)
    
        if(v4_match or v6_match):		# check if value is valid IPv4 or IPv6 address
            coords = ip2geo.lookupIP(ip, _format="geojson")	# actual lookup
            if(coords is not False):		# If coordinates found, create a geodata record
                aRec = dict(location=coords, _id=str(document['_id']))
                #aRec = {"location": coords, "_id": str(document['_id'])}
                geoList.append(aRec)
            else:
                logging.debug('No coordinates found for "{0}".'.format(ip))

logging.debug('Found {0} addresses.'.format(len(geoList)))

## Load coordinates into MongoDB  ##
logging.debug('Begin loading coordinates into Mongo.')
store2Mongo(dbClient[config['db-name']], 'geodata', geoList)

