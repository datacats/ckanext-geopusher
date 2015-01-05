"""geopusher command line interface

Usage:
  geopusher start
  geopusher register CKAN_SITE_URL

Options:
  -c --config=CONFIG        Configuration file,

"""

import os
import jobs
import docopt
import ckanapi

import ckanserviceprovider.web as web

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
    elif opts['register']:
        ckan_url = arguments['CKAN_SITE_URL']
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
