import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model

import pylons.config as config
import pylons

import uuid

import ckanapi

from ckan.model.domain_object import DomainObjectOperation
from ckan.plugins.toolkit import get_action

from ckan.lib.celery_app import celery


class GeopusherPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDomainObjectModification, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'geopusher')

    def notify(self, entity, operation=None):
        if isinstance(entity, model.Resource):
            resource_url = entity.url
            package_id = entity.package_id
            # new event is sent, then a changed event. 
            if operation == DomainObjectOperation.changed:
                # There is a NEW or CHANGED resource. We should check if
                # it is a shape file and pass it off to Denis's code if
                # so it can process it
                celery.send_task(
                    'geopusher.process_resource',
                    args=[resource_url, package_id],
                    task_id='{}-{}'.format(str(uuid.uuid4()), operation))
