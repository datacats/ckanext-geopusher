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

from docopt import doctopt
from ckanapi.remoteckan import RemoteCKAN
from ckanapi.localckan import LocalCKAN

def parse_arguments():
    return docopt(__doc__, version = __version__)

def main():
    arguments = parse_arguments()

    if arguments['--remote']:
        ckan = RemoteCKAN(arguments['--remote'], apikey=arguments['--apikey'])
    else:
        ckan = LocalCKAN(username=arguments['--user'])
