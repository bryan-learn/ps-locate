# ps_locate
A python tool which returns a list of the geographically closest registered perfSonar nodes.

# Dependencies
- MongoDB 3.2+

# Build
From root project directory run:
	'python setup.py build'

# Install
From root project directory run:
	'pip install .'

# Run
Syntax: ps_locate -i <IP Address> [-u <db url>] [-p <port>] [-d <db name>] [-c <host count>] [-o <output file>]
Example: ps_locate -i "182.128.160.10" -c 1
