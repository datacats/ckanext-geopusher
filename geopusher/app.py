from flask import Flask, request
from subprocess import call
app = Flask(__name__)

CKAN_URL = os.environ.get('CKAN_URL', 'http://boot2docker:5698')
APIKEY = os.environ.get('APIKEY', '3067dd7b-945f-44f4-a090-3c990a4ccd83')

@app.route('/', methods=['POST'])
def process_webhook():
    resource = json.loads(request.data).get('entity', None)
    if resource is None:
        return "", 400

    print "{0}".format(resource['name'])

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

        if os.path.getsize(outfile) > 20000000:
            return '', 413

        ckan = ckanapi.RemoteCKAN(CKAN_URL, apikey=APIKEY)
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

        return '', 201

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
