# Architecture Document for PS-Locate

## Components
1. Local perfSONAR Database 
	* MongoDB
	* Stores perfSONAR data and coordinate points
	* Uses geospatial index for quick nearest-neighbor searches on coordinate points
2. perfSONAR Database Update Agent
	* Python program: "src/<name>.py"
	* Interacts with ESnet's Simple-Lookup-Service to pull perfSONAR data
	* Writes perfSONAR data to Data Store
3. GeoLite2 Database Update Agent
	* Python program: "src/<name>.py"
	* Downloads the most recent version of the GeoLite2 database from MaxMind
3. Nearest Neighbor Query Agent
	* Python program: "src/<name>.py"
	* Interacts with Local perfSONAR Database to find the closest perfSONAR nodes to a given IP

## Workflows
Monthly: Update GeoLite2 Database

1. Update geolite2 database
	* "src/updateGeoIpDB.sh"
	* GeoLite2 database is updated the first Tuesday for each month

Nightly: Update local perfSONAR Database

1. Pull all perfSONAR records for simple-lookup-service
2. Load perfSONAR records into Data Store
3. Lookup geographical coordinates for each perfSONAR host
	* update host records in Data Store with coordinates

User / On-demand: Find closest perfSONAR nodes

1. Take an input IP address
2. Search Data Store for nearest N perfSONAR nodes
3. Search Data Store for meta data for each returned node
4. Output perfSONAR nodes and meta data to user
