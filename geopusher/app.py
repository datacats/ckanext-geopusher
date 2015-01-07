import uuid
import json
import shutil
import ckanapi
import logging
import requests
import shapefile

from flask import Flask, request
app = Flask(__name__)

def convert_file(shapefile_path, outfile_path):
    reader = shapefile.Reader(shapefile_path)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
       atr = dict(zip(field_names, sr.record))
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    geojson = open(outfile_path, "w")
    geojson.write(json.dumps(
                    {"type": "FeatureCollection",
                     "features": buffer
                    },
                  indent=2) + "\n"
                  )
    geojson.close()

def download_file(url):
    tmpname = 'tmp/{0}.{1}'.format(uuid.uuid1(), 'zip')
    response = requests.get(url, stream=True)
    with open(tmpname, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    return tmpname

@app.route('/', methods=['POST'])
def process_webhook():
    resource = json.loads(request.data).get('entity', None)
    if resource is None:
        return "", 400

    if resource.get('format', None) == 'SHP':
        file = download_file(resource['url'])

        outfile = "tmp/out/{0}.{1}".format(resource['name'], 'json')
        convert_file(file, outfile)

        ckan.action.resource_create(
            package_id = resource['package_id'],
            upload = open(outfile),
            format = 'GeoJSON',
            name = resource['name']
        )

    return '', 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
