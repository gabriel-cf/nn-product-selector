from .modules.keras_learning.training.catalog_trainer import CatalogTrainer
from .modules.task_scheduler.scheduler import Scheduler
from .modules.recommender_engine.recommender_engine import RecommenderEngine
from .modules.dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO - Increase when in prod
dMAX = 10

class Loader(object):
    """This class is meant to be loaded by an import in the product_selector.urls module
       Will make the first training of the NN
    """
    # Train the NN and load the rules from DB
    CatalogTrainer.trainNN(updateRules=True)
    scheduler = Scheduler()
    scheduler.scheduleUpdateRates()
    scheduler.scheduleUpdateNN()
    scheduler.scheduleUpdatePredictions(immediate=True) # To run when startup
    scheduler.scheduleUpdatePredictions(immediate=False) # To run periodically in the future
    scheduler.start()
