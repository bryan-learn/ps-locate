'''
Loads in json records written by 'get-all-records.py' script.
Inserts host, service, and interface records into MongoDB in seperate collections.
Creates seperate collection 'corrleated' for quick lookup of values related to a unique host.
Local MongoDB config:
- database: staging
- collections: hosts, services, interfaces, correlated
'''

#from memory_profiler import profile
import logging
import pymongo
import json

config = {
    'db-url': "mongodb://localhost",
    'db-port': 27017,
    'db-name': "staging"
}

#@profile
def readAll():
    hRec = open('data/hostRecords.json', 'r')
    hJson = json.loads(hRec.read())
    hRec.close()
    
    sRec = open('data/serviceRecords.json', 'r')
    sJson = json.loads(sRec.read())
    sRec.close()
    
    iRec = open('data/interfaceRecords.json', 'r')
    iJson = json.loads(iRec.read())
    iRec.close()

    return hJson, sJson, iJson;

def connectToMongodb():
    # config mongodb connection and database to use
    url = config['db-url'] +":"+ str(config['db-port'])
    client = pymongo.MongoClient(url)
    return client

def indexConfig(db):
    db['hosts'].create_index([
        ("uri", pymongo.TEXT),
        ("host-net-interfaces", pymongo.TEXT)
    ])
    db['interfaces'].create_index([
        ("uri", pymongo.TEXT)
    ])
    db['services'].create_index([
        ("service-host", pymongo.TEXT)
    ])

#@profile
def store2Mongo(db, collectionStr, records):
    # use collection from collectionStr; creates collection if doesn't exist
    coll = db[collectionStr]
    result = coll.insert_many(records)
    
    return result

## Setup Mongo DB ##
dbClient = connectToMongodb()			# connect to local mongo db
dbClient.drop_database(config['db-name'])	# delete old 'staging' db to clear out old content
indexConfig(dbClient[config['db-name']])	# set up indexes for new collections

## Read Records from File - Load into Mongo DB ##
hostRecords = []
serviceRecords = []
interfaceRecords = []

hostRecords, serviceRecords, interfaceRecords = readAll() 				# read in all record files
result = store2Mongo(dbClient[config['db-name']], 'hosts', hostRecords)			# write host records to mongo
result = store2Mongo(dbClient[config['db-name']], 'services', serviceRecords)		# write service records to mongo
result = store2Mongo(dbClient[config['db-name']], 'interfaces', interfaceRecords)	# write interface records to mongo

## Add collection (table) of correlated key fields for easier lookups ##
'''
Example record in correlated collection:
{
    _id: "<host-uri>",			# host.uri / service.services-host
    addresses: [<ip-address>,...],	# interface.interface-addresses
    interfaces: [<interface-uri>,...]	# interface.uri / host.host-net-interfaces
}
'''

db = dbClient[config['db-name']]
cursor = db.hosts.aggregate([
    {"$project": {"host-net-interfaces": 1, "uri": 1}},		# only grab key fields from hosts
    {"$unwind": "$host-net-interfaces"},			# unravel the array 'host-net-interfaces'
    {"$lookup": {						# left outer join on interfaces
        "from": "interfaces",
        "localField": "host-net-interfaces",
        "foreignField": "uri",
        "as": "ifaces"
    }},
    {"$group": {						# group by host uri (id). This undoes the unwind step.
        "_id": "$uri",
        "interfaces": {"$push": "$host-net-interfaces"},	# include the interface ids
        "addresses": {"$push": "$ifaces.interface-addresses"}	# include the interface addresses
    }},
    {"$out": "correlated"}					# store result in new collection, 'correlated'
])

