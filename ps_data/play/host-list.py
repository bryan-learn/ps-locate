import json
from sls_client.records import *
from sls_client.query import *

queryString = 'type=interface&host-name=ps.ac.lk'
response = query(queryString)
for res in response:
    print("=========================================")
    for key in res:
        print( key+": "+json.dumps(res[key]) )

