from .modules.keras_learning.training.catalog_trainer import CatalogTrainer

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
    
