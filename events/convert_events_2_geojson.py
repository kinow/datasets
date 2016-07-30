#!/usr/bin/env python

import json
from geojson import Point

from pprint import pprint

with open('./events_chch_201608.json') as infile:
    with open('./events_chch_201608.geojson', 'w') as outfile:
        j = json.load(infile)

        for event in j:
            if event['point'] != None:
                if event['point']['lat'] != None and event['point']['lng']:
                    point = Point((float(event['point']['lat']), float(event['point']['lng'])))
                    pprint(event)
                    break
