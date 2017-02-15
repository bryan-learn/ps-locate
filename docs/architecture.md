# Architecture Document for PS-Locate

## Components
1. Local perfSONAR Database 
	* MongoDB
	* Stores perfSONAR data and coordinate points
	* Uses geospatial index for quick nearest-neighbor searches on coordinate points
2. perfSONAR Database Update Agent
	* Python program: "src/update_perfsonar_data.sh"
	* Interacts with ESnet's Simple-Lookup-Service to pull perfSONAR data
	* Writes perfSONAR data to Data Store
3. GeoLite2 Database Update Agent
	* Python program: "src/update_geo_ip_db.sh"
	* Downloads the most recent version of the GeoLite2 database from MaxMind
4. Geo Location Update Agent
	* Python program: "src/geolocate/populate_ps_geoip.py"
	* Looks up and adds geographical coordinates to all perfSONAR host records
5. Nearest Neighbor Query Agent
	* Python program: "src/geolocate/ps_locate.py"
	* Interacts with Local perfSONAR Database to find the closest perfSONAR nodes to a given IP


## Workflows
Update GeoLite2 Database (Monthly: update_geo_ip_db.sh)
  
1. GeoLite2 Database Update Agent
	* Agent is executed manually or by scheduled job to update the database
	* MaxMind updates the GeoLite2 database on the first Tuesday of each month

Update local perfSONAR Database (Nightly: update_perfsonar_data.sh)

1. perfSONAR Database Update Agent
	* Pull all perfSONAR records from simple-lookup-service
	* Load perfSONAR records into 'staging' Data Store
2. Geo Location Update Agent
	* Lookup geographical coordinates for each perfSONAR host (each interface per host)
	* Create collection 'geodata' in 'staging' Data Store for storing geojson coordinates
3. perfSONAR Database Update Agent
	* Remove 'old-ps-data' Data Store
	* Copy 'ps-data' Data Store to 'old-ps-data' Data Store
	* Copy 'staging' Data Store to 'ps-data' Data Store

Find closest perfSONAR nodes (User/On Demand: ps_locate)

1. Nearest Neighbor Query Agent
	* Take an input IP address
	* Search Data Store for nearest N perfSONAR nodes
	* Search Data Store for meta data for each returned node
	* Output perfSONAR nodes and meta data to user

