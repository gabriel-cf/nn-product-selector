"""
    Task scheduler
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from .jobs.db_update_rates import DBUpdateRates
from .jobs.nn_update_network import NNUpdateNetwork

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Scheduler(object):
    # misfire_grace_time will prevent one job for not being fired if it overlaps with another
    MISFIRE_GRACE_TIME = 3600
    def __init__(self, job_l):
        executors = {
            # We only allow one execution per time to avoid conflicts
            'default': ThreadPoolExecutor(1),
        }
        self._scheduler = BackgroundScheduler(executors=executors)
        for job, hours in job_l:
            logger.info("Adding job %s executing every %d hours", job.__name__, hours)
            self._scheduler.add_job(job, 'interval', hours=hours, coalesce=True, misfire_grace_time=3600)

    def addJob(self, job, hours):
        logger.info("Adding job %s executing every %d hours", job.__name__, hours)
        self._scheduler.add_job(job, 'interval', hours=hours, coalesce=True,
                                misfire_grace_time=Scheduler.MISFIRE_GRACE_TIME)

    def scheduleUpdateRates(self, hours=3):
        self.addJob(DBUpdateRates.job, hours)

    def scheduleUpdateNN(self, hours=24):
        self.addJob(NNUpdateNetwork.job, hours)

    def start(self):
        self._scheduler.start()
