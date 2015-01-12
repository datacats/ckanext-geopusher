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
