import os
import uuid
import json
import shutil
import ckanapi
import zipfile
import logging
import requests
import shapefile

from flask import Flask, request
from subprocess import call
app = Flask(__name__)

TEMPDIR = 'tmp'
OUTDIR = os.path.join(TEMPDIR, 'out')

CKAN_URL = os.environ.get('CKAN_URL', None)
APIKEY = os.environ.get('APIKEY', None)

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

@app.route('/', methods=['POST'])
def process_webhook():
    resource = json.loads(request.data).get('entity', None)
    if resource is None:
        return "", 400

    if resource.get('format', None) == 'SHP':
        file = download_file(resource['url'])

        unzipped_dir = unzip_file(file)

        shapefile = None
        for f in os.listdir(unzipped_dir):
            if f.endswith(".shp"):
                shapefile = f

        outfile = os.path.join(OUTDIR,
                              "{0}.{1}".format(resource['name'], 'json'))

        convert_file(os.path.join(unzipped_dir, shapefile), outfile)

        ckan = ckanapi.RemoteCKAN(CKAN_URL, apikey=APIKEY)

        package = ckan.action.package_show(id=resource['package_id'])
        for res in package['resources']:
            if res['format'] == 'GeoJSON':
                ckan.action.resource_delete(id=res['id'])

        ckan.action.resource_create(
            package_id = resource['package_id'],
            upload = open(outfile),
            format = 'GeoJSON',
            name = resource['name'],
            url = 'any'
        )

        return '', 201

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
