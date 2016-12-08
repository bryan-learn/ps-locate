# Architecture Document for PS-Locate

## Components
1. Local perfSONAR Database 
	* MongoDB
	* Stores perfSONAR data and coordinate points
	* Uses geospatial index for quick nearest-neighbor searches on coordinate points
2. perfSONAR Database Update Agent
	* Python program: "src/update-ps-store.py"
	* Interacts with ESnet's Simple-Lookup-Service to pull perfSONAR data
	* Writes perfSONAR data to Data Store
3. GeoLite2 Database Update Agent
	* Python program: "src/update-geoip-store.py"
	* Downloads the most recent version of the GeoLite2 database from MaxMind
4. Geo Location Update Agent
	* Python program: "src/populate-ps-geoip.py"
	* Looks up and adds geographical coordinates to all perfSONAR host records
5. Nearest Neighbor Query Agent
	* Python program: "src/ps-locate.py"
	* Interacts with Local perfSONAR Database to find the closest perfSONAR nodes to a given IP

## Workflows
Monthly: Update GeoLite2 Database

1. GeoLite2 Database Update Agent
	* Agent is executed manually or by scheduled job to update the database
	* MaxMind updates the GeoLite2 database on the first Tuesday of each month

Nightly: Update local perfSONAR Database

1. perfSONAR Database Update Agent
	* Pull all perfSONAR records for simple-lookup-service
	* Load perfSONAR records into Data Store
2. Geo Location Update Agent
	* Lookup geographical coordinates for each perfSONAR host
	* update host records in Data Store with coordinates

User / On-demand: Find closest perfSONAR nodes

1. Nearest Neighbor Query Agent
	* Take an input IP address
	* Search Data Store for nearest N perfSONAR nodes
	* Search Data Store for meta data for each returned node
	* Output perfSONAR nodes and meta data to user

