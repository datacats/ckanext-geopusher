import logging

import ckanserviceprovider.job as job
import ckanserviceprovider.util as util

@job.async
def process_resource_notifications(task_id, input, dry_run=False):
    print 'hello'
