'''
Meant to be run after staging data is complete.
Copies 'ps-data' to 'old-ps-data'.
Copies 'staging' to 'ps-data'.
'''

import pymongo
import json

config = {
    'db-url': "mongodb://localhost",
    'db-port': 27017
}

def connectToMongodb():
    # config mongodb connection and database to use
    url = config['db-url'] +":"+ str(config['db-port'])
    client = pymongo.MongoClient(url)
    return client

## Rotate Databases ##
dbClient = connectToMongodb()           				# connect to local mongo db
dbClient.drop_database('old-ps-data')					# delete 'old-ps-data' db
dbClient.admin.command('copydb', fromdb='ps-data', todb='old-ps-data') 	# copy current 'ps-data' to 'old-ps-data'
dbClient.drop_database('ps-data')					# delete 'ps-data' db
dbClient.admin.command('copydb', fromdb='staging', todb='ps-data')	# copy 'staging' to 'ps-data'

