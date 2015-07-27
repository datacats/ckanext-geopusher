import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model

from ckan.model.domain_object import DomainObjectOperation


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
            if not operation:
                # There was no operation on the resource
                # TODO: Check in CKAN's source code for when this fires.
                return
            elif operation == DomainObjectOperation.new:
                # There is a NEW resource. We should check if it is 
                # a shape file and pass it off to Denis's code if 
                # so
                pass
            elif operation == DomainObjectOperation.changed:
                # There is a MODIFIED resource. Same as above.
                pass
