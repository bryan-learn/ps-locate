from random import random
import json

pointCnt = 10000

points = []

# create random items
print "Adding %i points to system" % (pointCnt)
for num in range(0,pointCnt):
    tLat = random()*180-90
    tLong = random()*360-180
    points.append([tLong, tLat])

geojsonList = []
for p in points:
    record = {
        "loc": {"type": "Point", "coordinates": [p[0], p[1]]},
        "label": "fake point"
    }
    geojsonList.append(record)

with open('data/geojson.json', 'w') as outfile:
    json.dump(geojsonList, outfile)

