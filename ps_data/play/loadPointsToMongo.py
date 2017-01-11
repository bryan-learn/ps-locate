from memory_profiler import profile
import pymongo
import json

hostRecords = []
serviceRecords = []
interfaceRecords = []

@profile
def readAll():
	geoRec = open('data/geojson.json', 'r')
	geoJson = json.loads(geoRec.read())
	geoRec.close()

	return geoJson;

def connectToMongodb():
	#config mongodb connection and database to use
	client = pymongo.MongoClient("mongodb://localhost:27017")
	db = client['geodata']
	return db

@profile
def store2Mongo(db, collectionStr, records):
	#use collection from collectionStr; creates collection if doesn't exist
	coll = db[collectionStr]
	result = coll.insert_many(records)
	
	return result

dbClient = connectToMongodb()

# Load records from file
geoRecords = readAll()

# Create 2dSphere index for collection
dbClient.testPoints.create_index([("loc", pymongo.GEOSPHERE)])

# Insert documents into our db
result = store2Mongo(dbClient, 'testPoints', geoRecords)

