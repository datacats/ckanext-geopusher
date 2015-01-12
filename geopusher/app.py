import ckanapi

from lib import process, FileTooLargeError
from flask import Flask, request
app = Flask(__name__)

CKAN_URL = os.environ.get('CKAN_URL', 'http://boot2docker:5698')
APIKEY = os.environ.get('APIKEY', '3067dd7b-945f-44f4-a090-3c990a4ccd83')

@app.route('/', methods=['POST'])
def process_webhook():
    resource = json.loads(request.data).get('entity', None)
    if resource is None:
        return "", 400

    if resource.get('format', None) == 'SHP':
        print "processing {0}".format(resource['name'])

        ckan = ckanapi.RemoteCKAN(CKAN_URL, apikey=APIKEY)
        try:
            process(ckan, resource)
        except FileTooLargeError():
            return '', 413

        return '', 201

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
