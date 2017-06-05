import time
import logging
from ..dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ..dataset_processing.src.mapper.dbmapper import DBMapper
from ..dataset_processing.src.mapper.mapper import Mapper
from ..keras_learning.nn import NN
from ..keras_learning.io.nninput import NNInput
from ..keras_learning.io.nnoutput import NNOutput
from .categoryset import CategorySet
from .db_to_nn_input_processor import DBToNNInputProcesor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RecommenderEngine(object):
    """This static class handles the whole recommendation process since the call
       from the API is made. For a given user, it goes through the product
       catalog getting the predictions from the NN and returning a list
       of recommended categories with recommended products.
    """

    PRODUCT_CATEGORIES = Mapper.getAllAvailableCategories()

    @staticmethod
    def _getUserFromDB(dbUser):
        mUser = DBMapper.fromDBResultToMappedUser(dbUser)
        if mUser is None:
            logging.warn("Could not map user %s" % mUser)
        return mUser

    @staticmethod
    def _processCatalog(dbUser):
        """Returns generator of n NNInputSet of size {MAX_NN_INPUT_SIZE} values for a given user"""
        mUser = DBMapper.fromDBResultToMappedUser(dbUser)
        if mUser is None:
            logging.warn("Could not map user %s" % mUser)
            return
        productCursor = MongoHandler.getInstance().getAllProducts()
        exhausted = False
        while not exhausted:
            nnInputSet = DBToNNInputProcesor.generateIncrementalNNInputSet(mUser, productCursor)
            exhausted = nnInputSet.isEmpty()
            if not exhausted:
                yield nnInputSet

    @staticmethod
    def _processCatalogByCategories(dbUser):
        mUser = DBMapper.fromDBResultToMappedUser(dbUser)
        if mUser is None:
            logging.warn("Could not map user %s" % mUser)
            return
        for category in RecommenderEngine.PRODUCT_CATEGORIES:
            productCursor = MongoHandler.getInstance().getProductsByParameters(category=category)
            nnInputSet = DBToNNInputProcesor.generateSingleNNInputSet(mUser, productCursor)
            yield nnInputSet

    @staticmethod
    def getCategoriesForUser(username):
        ini = time.time()
        dbUser = MongoHandler.getInstance()\
                             .getUsersByParameters(one_only=True,
                                                   username=username)
        if not dbUser:
            logger.warning("No users were found for username '%s'" % username)
            return None
        nn = NN.getInstance()
        for nnInputSet in RecommenderEngine._processCatalogByCategories(dbUser):
            prediction = nn.predict(nnInputSet.getNNValues())
            prediction = NNOutput.translatePredictionListToDecimalList(prediction)
            products = nnInputSet.getMappedProducts()
            productPredictionList = zip(products, prediction)
            print(productPredictionList)
        fini = time.time()
        print("Woao! we made it!")
        print(fini - ini)
