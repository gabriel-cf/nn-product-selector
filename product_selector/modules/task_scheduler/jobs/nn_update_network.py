import logging
import time
from ...keras_learning.nn import NN
from ...keras_learning.training.catalog_trainer import CatalogTrainer
from ...dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ...dataset_processing.src.mapper.dbmapper import DBMapper


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNUpdateNetwork(object):
    """Trains a new NN and replaces the active one when it is done"""
    @staticmethod
    def job():
        logger.info("Updating NN")
        ini = time.time()
        CatalogTrainer.trainNN()
        fini = time.time()
        logger.info("Completed in: %ds", (fini - ini))
