"""geopusher command line interface

Usage:
  geopusher start

Options:
  -c --config=CONFIG        Configuration file,

"""

import os
import docopt

import ckanserviceprovider.web as web

import jobs

# check whether jobs have been imported properly
assert(jobs.push_to_datastore)

def serve():
    web.init()
    web.app.run(web.app.config.get('HOST'), web.app.config.get('PORT'))

def main():
    opts = docopt(__doc__)

    cfg = arguments['--config']
    os.environ['JOB_CONFIG'] = cfg

    if opts['start']:
        serve()

if __name__ == '__main__':
    main()
