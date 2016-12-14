'''
Queries Mongo for list of all IP addresses in the interface records.
Looks up coordinates for each IP address then inserts the geojson format into 'geodata' collection.
Example geodata record:
{
    "location": {"type": "Point", "coordinates": [180, 90]},
    "net-uri": "<id>"
}
'''

#from memory_profiler import profile
import pymongo
import json
import re
import ip2geo

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


i=0
geoList = []
for document in cursor:
    ipList = document['addresses'][0]
    for ip in ipList:
        ip = str(ip[0])
        v4_match = re.match( ipv4_pattern, ip)
        v6_match = re.match( ipv6_pattern, ip)
    
        if(v4_match or v6_match):	# check if value is valid IPv4 or IPv6 address
            coords = ip2geo.lookupIP(ip)
            if(coords is not False):
                geoList.append(coords)
            else:
                print "no coordinates found for:", ip

print len(geoList)
