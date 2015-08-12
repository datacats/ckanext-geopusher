from ckan.lib.celery_app import celery
from requests import get
from lib import process

import ckanapi

@celery.task(name='geopusher.process_resource')
def process_resource(resource_id, site_url, apikey):
    ckan = ckanapi.RemoteCKAN(site_url, apikey=apikey)
    print("processing resource {0}".format(resource_id))
    process(ckan, resource_id)
