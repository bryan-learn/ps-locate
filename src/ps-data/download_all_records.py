'''
Queries records from simple-lookup-service and writes seperate record types
to seperate json files in the data directory.
Types:
- host		--> hostRecords.json
- interface 	--> interfaceRecords.json
- service 	--> serviceRecords.json
'''
import json
import re
from sls_client.records import *
from sls_client.query import *
from sls_client.find_host_info import *

#query all host records
queryStr = 'type=host'
result = query(queryStr)
jsonRes = json.dumps(result)

file = open('data/hostRecords.json', 'w')
file.write(jsonRes)
file.close()

#query all interface records
queryStr = 'type=interface'
result = query(queryStr)
jsonRes = json.dumps(result)

file = open('data/interfaceRecords.json', 'w')
file.write(jsonRes)
file.close()

#query all service records
queryStr = 'type=service'
result = query(queryStr)
jsonRes = json.dumps(result)

file = open('data/serviceRecords.json', 'w')
file.write(jsonRes)
file.close()

