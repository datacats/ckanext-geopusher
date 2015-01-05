"""geopusher command line interface

Usage:
  geopusher start [-c CONFIG]
  geopusher register CKAN_SITE_URL

Options:
  -c --config=CONFIG        Configuration file,

"""

import os
import jobs
import ckanapi

from docopt import docopt
import ckanserviceprovider.web as web

def serve():
    web.init()
    web.app.run(web.app.config.get('HOST'), web.app.config.get('PORT'))

def main():
    opts = docopt(__doc__)

    if opts['start']:
        cfg = opts['--config']
        os.environ['JOB_CONFIG'] = cfg
        serve()
        
    elif opts['register']:
        ckan_url = opts['CKAN_SITE_URL']
        geopusher_url = "http://{0}:{1}/".format(web.app.config.get('HOST'),
                                                 web.app.config.get('PORT'))

        ckan = ckanapi.RemoteCKAN(ckan_url)
        webhook = ckan.action.webhook_create(
            topic = 'resource/create',
            address = geopusher_url
        )

        print "registered webhook {0} with {1}".format(webhook, ckan_url)

if __name__ == '__main__':
    main()
