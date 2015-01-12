"""command line utility for geopusher

Usage:
    geopusher import (ID_OR_NAME ... | --all)
              [[-c CONFIG] [-u USER] | -r CKAN_URL [-a APIKEY]]

Options:
    -h --help               show help
    --version               show version
    -a --apikey=APIKEY      Your CKAN API key
    -c --config=CKAN_INI    Path to local CKAN ini file (default development.ini)
    -u --user=CKAN_USER     Name of CKAN user to use (local CKAN only)
    -r --remote=CKAN_URL    Remote CKAN url
    --all                   Convert all datasets on a CKAN instance
"""

from docopt import docopt
from ckanapi.remoteckan import RemoteCKAN
from ckanapi.localckan import LocalCKAN

from geopusher.version import __version__
from geopusher.lib import convert_and_import

def parse_arguments():
    return docopt(__doc__, version = __version__)

def main(paster=False):
    arguments = parse_arguments()

    if not paster and not arguments['--remote']:
        return _switch_to_paster(arguments)

    if arguments['--remote']:
        ckan = RemoteCKAN(arguments['--remote'], apikey=arguments['--apikey'])
    else:
        ckan = LocalCKAN(username=arguments['--user'])

    if arguments['import']:
        if arguments['--all']:
            convert_and_import(ckan, ckan.action.package_list())
        else:
            convert_and_import(ckan, arguments['ID_OR_NAME'])


def _switch_to_paster(arguments):
    sys.argv[1:1] = ['--plugin=geopusher', 'geopusher']
    sys.exit(load_entry_point('PasteScript', 'console_scripts', 'paster')())
