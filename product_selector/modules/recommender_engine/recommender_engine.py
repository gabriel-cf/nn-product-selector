import logging
from ..dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ..dataset_processing.src.mapper.dbmapper import DBMapper
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

    @staticmethod
    def _translate(self, arg):
        pass

    @staticmethod
    def _processCatalog(dbUser):
        """Returns generator of n NNInputSet of size {MAX_NN_INPUT_SIZE} values for a given user"""
        mUser = DBMapper.fromDBResultToMappedUser(dbUser)
        if mUser is None:
            logging.warn("User %s not found" % mUser)
            return
        productCursor = MongoHandler.getInstance().getAllProducts()
        exhausted = False
        while not exhausted:
            nnInputSet = DBToNNInputProcesor.generateNNInputSet(mUser, productCursor)
            exhausted = nnInputSet.isEmpty()
            if not exhausted:
                yield nnInputSet

    @staticmethod
    def getRecommendationsForUser(username):
        dbUser = MongoHandler.getInstance()\
                             .getUsersByParameters(one_only=True,
                                                   username=username)
        if not dbUser:
            logger.warning("No users were found for username '%s'" % username)
            return None
        nn = NN.getInstance()
        for nnInputSet in RecommenderEngine._processCatalog(dbUser):
            prediction = nn.predict(nnInputSet.getValues())
            prediction = NNOutput.translatePredictionListToDecimalList(prediction)
            print(prediction)
        print("Woao! we made it!")
