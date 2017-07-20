import logging
from itertools import islice
from ..settings_loader import SettingsLoader
from ..dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ..dataset_processing.src.mapper.dbmapper import DBMapper
from ..dataset_processing.src.model.mappeduser import MappedUser
from ..dataset_processing.src.model.mappedproduct import MappedProduct
from ..keras_learning.io.nninputset import NNInputSet
from ..keras_learning.io.nninput import NNInput

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBToNNInputProcesor(object):
    """"""
    @staticmethod
    def getNNInputGenerator(mUser, productCursor, category=None):
        def generator():
            for dbProduct in productCursor:
                mProduct = DBMapper.fromDBResultToMappedProduct(dbProduct)
                if mProduct and mProduct.hasCategory():
                    nnInputValue = NNInput.getNNValues(mUser, mProduct, only_entry=False)
                    yield nnInputValue, mProduct
        return generator
