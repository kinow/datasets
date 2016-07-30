#!/usr/bin/env python

import json
import geojson

from pprint import pprint

with open('./events_chch_201608.json') as infile:
    with open('./events_chch_201608.geojson', 'w') as outfile:
        j = json.load(infile)

        features = []
        for event in j:
            if event['point'] != None:
                if event['point']['lat'] != None and event['point']['lng']:
                    # properties
                    props = event.copy()
                    del props['point']
                    # geometry
                    point = geojson.Point((float(event['point']['lng']), float(event['point']['lat'])))
                    # and feature
                    f = geojson.Feature(geometry=point, properties=props)
                    features.append(f)

        feature_col = geojson.FeatureCollection(features, crs="EPSG:4326")

        json.dump(feature_col, outfile)
