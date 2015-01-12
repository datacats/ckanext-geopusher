import os
import uuid
import json
import shutil
import ckanapi
import zipfile
import logging
import requests
import shapefile

TEMPDIR = 'tmp'
OUTDIR = os.path.join(TEMPDIR, 'out')

def convert_file(shapefile_path, outfile_path):
    if os.path.isfile(outfile_path):
        os.remove(outfile_path)

    call(['ogr2ogr', '-f', 'GeoJSON', '-t_srs', 'crs:84',
            outfile_path, shapefile_path ])

def download_file(url):
    tmpname = '{0}.{1}'.format(uuid.uuid1(), 'shp.zip')
    response = requests.get(url, stream=True)
    with open(os.path.join(TEMPDIR, tmpname), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    return tmpname

def unzip_file(filepath):
    z = zipfile.ZipFile(os.path.join(TEMPDIR, filepath))
    dirname = os.path.join(TEMPDIR, filepath[:-4])
    os.makedirs(dirname)
    for name in z.namelist():
        z.extract(name, dirname)

    return dirname
