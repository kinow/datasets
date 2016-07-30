#!/usr/bin/env python

# Convert datasets from 2193 to 4326

import os, sys
import glob
import fiona
import fiona.crs

def main():
    for file in glob.glob('./**/*.geojson', recursive=True):
        file_name = os.path.basename(file)
        destination_file_name = file_name
        destination_file_name = destination_file_name.lower()

        with fiona.open(file) as source:
            with fiona.open(destination_file_name, 'w', driver='GeoJSON', crs=fiona.crs.from_epsg(4326), schema=source.schema) as sink:
                for rec in source:
                    sink.write(rec)


if __name__ == '__main__':
    main()
