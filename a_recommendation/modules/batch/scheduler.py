"""
    Task scheduler
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Scheduler(object):
    def __init__(self, job_l):
        executors = {
            # We only allow one execution per time to avoid conflicts
            'default': ThreadPoolExecutor(1),
        }
        self._scheduler = BackgroundScheduler(executors=executors)
        for job, hours in job_l:
            logger.info("Adding job %s executing every %d hours", job.__name__, hours)
            # misfire_grace_time will prevent one job for not being fired if it overlaps with another
            self._scheduler.add_job(job, 'interval', hours=hours, coalesce=True, misfire_grace_time=3600)
            #self._scheduler.add_job(job, 'interval', hours=hours, coalesce=True, misfire_grace_time=3600)

    def start(self):
        self._scheduler.start()
