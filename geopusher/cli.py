"""command line utility for geopusher

Usage:

"""
import ckanapi

from docopt import doctopt

def main():
    arguments = docopt(__doc__, version=__version__)
