import pylons.config as config
import ckan.plugins as p
import paste.script
import logging
import ckanapi

from ckan.lib.cli import CkanCommand
from lib import process
from ckan import model

log = logging.getLogger(__name__)

class GeopusherCommands(CkanCommand):
    """
    ckanext-geopusher commands:

    Usage::

        paster geopusher convert <resource_id>
        paster geopusher convertall
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__

    parser = paste.script.command.Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', dest='config',
        default='development.ini', help='Config file to use.')

    def command(self):
        if not len(self.args):
            print self.__doc__
            return

        cmd = self.args[0]
        self._load_config()

        site_url = config.get('ckan.site_url', 'http://localhost')
        apikey = model.User.get('default').apikey
        ckan = ckanapi.RemoteCKAN(site_url, apikey=apikey)

        if cmd == 'convertall':
            self._convertall(ckan)
        elif cmd == 'convert':
            self._convert(ckan, self.args[1])
        else:
            print self.__doc__

    def _convertall(self, ckan):
        for package in ckan.action.package_list():
            resources = ckan.action.package_show(id=package).get('resources', [])
            for resource in resources:
                print("converting resource {} for package {}".format(resource['id'], resource['package_id']))
                self._convert(ckan, resource['id'])
            

    def _convert(self, ckan, resource_id):
        process(ckan, resource_id)
