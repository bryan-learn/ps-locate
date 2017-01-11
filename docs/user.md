Basic Usage:
	ps_locate.py -i <IP Address> [-u <db url>] [-p <port>] [-d <db name>] [-c <host count>] [-o <output file>]

Examples:
	1) $python ps_locate.py -i "128.182.1.160"
		- Most basic usage. Assumes default values if only the IP is provided.
		Defaults:
			-u "mongodb://localhost"
			-p 27017
			-d "ps-data"
			-c 3

	2) $python ps_locate.py -i "128.182.1.160" -c 3 -o "result.json"

Output Description:
	The output json is an array of custom JSON objects.
	Each element of that array has three top-level fields: "services", "interfaces", and "host".

        [{
	    "services": [],	// Array of perfSONAR records
	    "interfaces": [],	// Array of perfSONAR records
            "host": {}		// Single perfSONAR record
	}]

	Root:
		An array of objects containing *all* data associated with a perfSONAR host. The length of this array is equal to the host-count (-c option of cli).
	Services:
		An array of service records from the perfSONAR database. Each record is associated with the host record.
	Interfaces:
		An array of interface records from the perfSONAR database. Each record is associated with the host record.
	Host:
		A perfSONAR host record.

	[TODO: add details about perfSONAR records. I.e., what fields each record type has, etc. For now look at es.net's resources: https://github.com/esnet/simple-lookup-service/wiki]