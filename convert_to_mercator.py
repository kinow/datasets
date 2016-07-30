#!/usr/bin/env python

# Convert datasets from 2193 to 4326

import os, sys
import glob
import ogr, osr, gdal

# Source: http://geoinformaticstutorial.blogspot.co.nz/2012/10/reprojecting-shapefile-with-gdalogr-and.html
# And: http://pcjericks.github.io/py-gdalogr-cookbook/gdal_general.html#install-gdal-ogr-error-handler

# export GDAL_DATA=/home/kinow/Development/python/anaconda3/share/gdal

# example GDAL error handler function
def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {
            gdal.CE_None:'None',
            gdal.CE_Debug:'Debug',
            gdal.CE_Warning:'Warning',
            gdal.CE_Failure:'Failure',
            gdal.CE_Fatal:'Fatal'
    }
    err_msg = err_msg.replace('\n',' ')
    err_class = errtype.get(err_class, 'None')
    print('Error Number: %s' % (err_num))
    print('Error Type: %s' % (err_class))
    print('Error Message: %s' % (err_msg))

def main():
    # install error handler
    gdal.PushErrorHandler(gdal_error_handler)

    for file in glob.glob('./**/*.geojson', recursive=True):
        file_name = os.path.basename(file)
        destination_file_name = file_name
        destination_file_name = destination_file_name.lower()

        driver = ogr.GetDriverByName('GeoJSON')

        # input SpatialReference
        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(2193)

        # output SpatialReference
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(4326)

        # create the CoordinateTransformation
        coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

        # get the input layer
        inDataSet = driver.Open(file)
        inLayer = inDataSet.GetLayer()

        # create the output layer
        outputShapefile = destination_file_name
        if os.path.exists(outputShapefile):
            driver.DeleteDataSource(outputShapefile)
        outDataSet = driver.CreateDataSource(outputShapefile)
        outLayer = outDataSet.CreateLayer("basemap_4326", geom_type=ogr.wkbMultiPolygon)

        # add fields
        inLayerDefn = inLayer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            outLayer.CreateField(fieldDefn)

        # get the output layer's feature definition
        outLayerDefn = outLayer.GetLayerDefn()

        # loop through the input features
        inFeature = inLayer.GetNextFeature()
        while inFeature:
            # get the input geometry
            geom = inFeature.GetGeometryRef()
            # reproject the geometry
            geom.Transform(coordTrans)
            # create a new feature
            outFeature = ogr.Feature(outLayerDefn)
            # set the geometry and attribute
            outFeature.SetGeometry(geom)
            for i in range(0, outLayerDefn.GetFieldCount()):
                outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
            # add the feature to the shapefile
            outLayer.CreateFeature(outFeature)
            # destroy the features and get the next input feature
            outFeature.Destroy()
            inFeature.Destroy()
            inFeature = inLayer.GetNextFeature()

        # close the shapefiles
        inDataSet.Destroy()
        outDataSet.Destroy()


if __name__ == '__main__':
    main()
