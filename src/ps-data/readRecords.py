from memory_profiler import profile
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

@profile
def correlateRecords(hosts, services, interfaces):
	db = []
	for h in hosts:
		tHost = ""
		tTests = ""
		if 'host-name' in h:
			tHost = h['host-name']
			for s in services:
				if 'serivce-host' in s:
					if h['uri'] == s['service-host']:
						tTests = s['service-type']
		db.append({"host": tHost, "tests": tTests})
	return db

hostRecords, serviceRecords, interfaceRecords = readAll()

#database = correlateRecords(hostRecords, serviceRecords, interfaceRecords)
