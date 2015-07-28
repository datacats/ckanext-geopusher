from ckan.lib.celery_app import celery
from requests import get

@celery.task(name='geopusher.process_resource')
def process_resource(resource_url, package_id):
    resp = get(resource_url, stream=True)
    print resp.raw.read()
