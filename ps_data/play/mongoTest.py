from pymongo import MongoClient

#connect to local mongodb instance
client = MongoClient("mongodb://localhost:27017")

#use database "test"
db = client['test']

#use collection "dataset"
coll = db['dataset']

#insert records into collection
result = coll.insert_one(
{"pshost-bundle": ["perfsonar-toolkit"], 
"host-net-tcp-autotunemaxbuffer-recv": ["33554432 bytes"], 
"host-os-kernel": ["Linux 2.6.32-642.1.1.el6.web100.x86_64"], 
"host-net-tcp-congestionalgorithm": ["reno"], 
"ttl": [], 
"client-uuid": ["62115a18-48c8-4893-849f-3bd1f04d4cf9"], 
"ls-host": "http://ps-west.es.net:8090/", 
"host-vm": ["1"], 
"host-hardware-processorspeed": ["2133.409 MHz"], 
"pshost-bundle-version": ["3.5.1.7"], 
"host-hardware-cpuid": ["Intel(R) Xeon(R) CPU E5506 @ 2.13GHz"], 
"location-sitename": ["SmarTone"], 
"host-administrators": ["lookup/person/f2fa2878-2af9-4bbe-b645-b13b25bb0295"], 
"host-net-tcp-autotunemaxbuffer-send": ["33554432 bytes"], 
"state": "renewed", 
"host-name": ["116.193.10.38"], 
"pshost-access-policy": ["private"], 
"pshost-toolkitversion": ["3.5.1.7"], 
"type": ["host"], 
"host-hardware-processorcore": ["1"], 
"host-os-version": ["6.8 (Final)"], 
"location-longitude": ["113.553900"], 
"host-net-interfaces": ["lookup/interface/1f6873a8-06ba-450b-aaeb-bc6cb5b4056b"], 
"host-manufacturer": ["VMware, Inc."], 
"expires": "2016-10-27T23:27:14.471Z", 
"location-city": ["Macau S.A.R."], 
"location-country": ["MO"], 
"pshost-role": ["site-border"], 
"host-hardware-processorcount": ["1"], 
"host-net-tcp-maxbuffer-send": ["67108864 bytes"], 
"host-productname": ["VMware Virtual Platform"], 
"host-hardware-memory": ["1877 MB"], 
"host-os-name": ["CentOS"], 
"uri": "lookup/host/b3c87970-85f4-46f4-a029-100ada5f4ca5", 
"group-domains": [], 
"location-latitude": ["22.188737"], 
"host-net-tcp-maxbuffer-recv": ["67108864 bytes"]
}
)

print result.inserted_id
