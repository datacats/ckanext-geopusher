Geopusher
=========
Capture any Shapefiles uploaded to CKAN and re-upload them as GeoJSON

Works well with ckanext-webhooks, or as a standalone command line utility which you can run periodically, with cron for example.

Installation
============
```
pip install -r requirements.txt
python setup.py develop
```
You will need GDAL. You can get in on Ubuntu with `apt-get install gdal-bin`

Usage
=====
### Command line

To create a GeoJSON resource from all the Shapefile resources on your CKAN
server:
```
geopusher import --all -r http://myckan.org -a your_api_key
```

To only convert resources for a subset of datasets:
```
geopusher import dataset1 dataset2 dataset3 -r http://myckan.org -a your_api_key
```

### Webhooks
Run the flask app in app.py. It needs to be deployed somewhere where CKAN
can reach it to notify it of new events.

You will need [ckanext-webhooks](https://github.com/deniszgonjanin/ckanext-webhooks)
enabled on your CKAN instance. Then register a webhook to be notified for
resource update events.

#### Example:
```
import ckanapi
ckan = ckanapi.RemoteCKAN('http://myckan.org', apikey='mykey')
ckan.action.webhook_create(address='http://geopusher.io', topic='resource/update')
```
