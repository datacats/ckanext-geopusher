import ckanapi
import json

from lib import process, FileTooLargeError
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_webhook():
    hook = json.loads(request.data)
    resource = hook.get('entity', None)
    if resource is None:
        return "", 400

    res_format = resource.get('format', None)

    if res_format == 'SHP' or res_format == 'KML':
        print "processing {0}".format(resource['name'].encode('utf-8'))

        ckan = ckanapi.RemoteCKAN(
                        hook.get('ckan', None),
                        apikey=hook.get('apikey', None))

        try:
            process(ckan, resource, res_format)
        except FileTooLargeError():
            return '', 413

        return '', 201

    return '', 200

@app.route('/', methods=['GET'])
def status():
    return 'Welcome to GeoPusher'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
