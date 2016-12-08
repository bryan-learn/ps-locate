from memory_profiler import profile
from pymongo import MongoClient
import json

hostRecords = []
serviceRecords = []
interfaceRecords = []

@profile
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
	#config mongodb connection and database to use
	client = MongoClient("mongodb://localhost:27017")
	db = client['ps-data']
	return db

@profile
def store2Mongo(db, collectionStr, records):
	#use collection from collectionStr; creates collection if doesn't exist
	coll = db[collectionStr]
	result = coll.insert_many(records)
	
	return result

dbClient = connectToMongodb()

hostRecords, serviceRecords, interfaceRecords = readAll()

result = store2Mongo(dbClient, 'hosts', hostRecords)
result = store2Mongo(dbClient, 'services', serviceRecords)
result = store2Mongo(dbClient, 'interfaces', interfaceRecords)

