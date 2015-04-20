import os
import uuid
import json
import shutil
import ckanapi
import zipfile
import logging
import requests
import shapefile

from subprocess import call

TEMPDIR = os.path.join(os.path.dirname(__file__), '..', 'tmp')
OUTDIR = os.path.join(TEMPDIR, 'out')

class BadResourceFileException(Exception):
    def __init__(self, extra_msg=None):
        self.extra_msg = extra_msg

    def __str__(self):
        return self.extra_msg

class FileTooLargeError(Exception):

    def __init__(self, extra_msg=None):
        self.extra_msg = extra_msg

    def __str__(self):
        return self.extra_msg

def convert_and_import(ckan, datasets, file_format):
    shutil.rmtree(TEMPDIR)

    for d in datasets:
        dataset = ckan.action.package_show(id=d)
        resources = dataset['resources']
        for resource in resources:
            res_name = resource['name'].encode('ascii', 'ignore')
            if resource['format'] == file_format:
                try:
                    print "processing {0}:{1}".format(d, res_name)
                    process(ckan, resource, file_format)
                except FileTooLargeError:
                    print "skipping {0}:{1} - too large".format(d, res_name)

def process(ckan, resource, file_format):
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    
    try:
        file = download_file(resource['url'], file_format)

        filepath = os.path.join(TEMPDIR, file)

        if file_format == 'SHP':
            unzipped_dir = unzip_file(file)

            shapefile = None
            for f in os.listdir(unzipped_dir):
                if f.endswith(".shp"):
                    shapefile = f

            if shapefile is None:
                print "No shapefile found in archive: {0}".format(unzipped_dir)
                return
            else:
                file = shapefile
                filepath = os.path.join(unzipped_dir, shapefile)


        res_name = resource['name'].encode('ascii', 'ignore')
        outfile = os.path.join(OUTDIR,
                              "{0}.{1}".format(res_name.replace('/', ''),
                              'json'))

        convert_file(filepath, outfile)

    except BadResourceFileException as e:
        return

    if os.path.getsize(outfile) > 20000000:
        raise FileTooLargeError()

    package = ckan.action.package_show(id=resource['package_id'])
    for res in package['resources']:
        if res['format'] == 'GeoJSON' and res['name'] == resource['name']:
            ckan.action.resource_delete(id=res['id'])

    ckan.action.resource_create(
        package_id = resource['package_id'],
        upload = open(outfile),
        format = 'GeoJSON',
        name = resource['name'],
        url = 'any'
    )

def convert_file(input_path, outfile_path):
    if os.path.isfile(outfile_path):
        os.remove(outfile_path)

    returncode = call(['ogr2ogr', '-f', 'GeoJSON', '-t_srs', 'crs:84',
            outfile_path, input_path ])

    if returncode == 1:
        raise BadResourceFileException(
            "{0} could not be converted".format(input_path)
        )

def download_file(url, file_format):
    if file_format == 'SHP':
        tmpname = '{0}.{1}'.format(uuid.uuid1(), 'shp.zip')
    elif file_format == 'KML':
        tmpname = '{0}.{1}'.format(uuid.uuid1(), 'kml')

    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise BadResourceFileException(
            "{0} could not be downloaded".format(url)
        )

    with open(os.path.join(TEMPDIR, tmpname), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    return tmpname

def unzip_file(filepath):
    try:
        z = zipfile.ZipFile(os.path.join(TEMPDIR, filepath))
    except zipfile.BadZipfile as e:
        raise BadResourceFileException(
            "{0} is not a valid zip file, skipping".format(filepath)
        )

    dirname = os.path.join(TEMPDIR, filepath[:-4])
    os.makedirs(dirname)
    for name in z.namelist():
        z.extract(name, dirname)

    return dirname
