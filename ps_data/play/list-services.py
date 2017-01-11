import json
import re
from sls_client.records import *
from sls_client.query import *
from sls_client.find_host_info import *

#query sls for every host record
queryString = 'type=service'
response = query(queryString)

#look at each service record.
for res in response:
	print res
