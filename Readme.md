Geopusher
=========
Capture any KML/Shapefiles uploaded to CKAN and re-upload them as GeoJSON

Implemented as a CKAN celery task that listens to resource updates

Installation
============
```
pip install -r requirements.txt
python setup.py develop
```
You will need GDAL. You can get in on Ubuntu with `apt-get install gdal-bin`

Usage
=====
```
$ datacats paster celeryd
```
