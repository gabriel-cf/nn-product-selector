import time
import logging
import numpy as np
from ..dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ..dataset_processing.src.mapper.dbmapper import DBMapper
from ..dataset_processing.src.mapper.mapper import Mapper
from ..dataset_processing.src.model.rating import Rating
from ..dataset_processing.src.model.category import Category
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
    def _getBestPredictedIndexes(predictions, max_results):
        ind = np.argpartition(predictions, -max_results)[-max_results:]
        ind = ind[np.argsort(predictions[ind])[::-1]]
        return ind

    @staticmethod
    def _getMappedUserFromUsername(username):
        dbUser = MongoHandler.getInstance()\
                             .getUsersByParameters(one_only=True,
                                                   username=username)
        if not dbUser:
            logger.warning("No users were found for username '%s'" % username)
            return None
        mUser = DBMapper.fromDBResultToMappedUser(dbUser)
        if not mUser:
            logging.warn("User %s was found but could not be mapped" % mUser)
            return None
        return mUser

    @staticmethod
    def _processCatalog(mUser):
        """Returns generator of n NNInputSet of size {MAX_NN_INPUT_SIZE} values for a given user"""
        productCursor = MongoHandler.getInstance().getAllProducts()
        nnInputGenerator = DBToNNInputProcesor.getNNInputGenerator(mUser, productCursor)
        return nnInputGenerator

    @staticmethod
    def _processCatalogByCategories(mUser):
        for category in RecommenderEngine.PRODUCT_CATEGORIES:
            productCursor = MongoHandler.getInstance().getProductsByParameters(category=category)
            nnInputGenerator = DBToNNInputProcesor.getNNInputGenerator(mUser, productCursor)

            yield nnInputGenerator, category

    @staticmethod
    def _getPredictedCategory(mUser, mProducts, predictions, max_results):
        max_results = len(predictions) if max_results > len(predictions) else max_results
        bestIndexes = RecommenderEngine._getBestPredictedIndexes(predictions, max_results)
        category_l = []
        for i in bestIndexes:
            expectedRating = Rating(mUser, mProducts[i], predictions[i])
            category_l.append(expectedRating)
        return category_l

    @staticmethod
    def getBestSelectionsForUser(username, max_results=10):
        mUser = RecommenderEngine._getMappedUserFromUsername(username)
        if not mUser:
            return
        nn = NN.getInstance()
        nnInputSet = RecommenderEngine._processCatalog(mUser)
        predictions = nn.predict(nnInputSet.getNNValues())
        predictions = NNOutput.translatePredictionListToDecimalList(predictions)
        mProducts = nnInputSet.getMappedProducts()
        bestSelections = RecommenderEngine._getPredictedCategory(mUser, mProducts, predictions, max_results)
        return bestSelections

    @staticmethod
    def _selectBestCategories(category_predictions_dict, max_categories=3):
        def calculateCategoryRating(category):
            total = 0
            for rating in category:
                total += rating.getRating()
            return total
        results = []
        for categoryName in category_predictions_dict:
            totalRating = calculateCategoryRating(category_predictions_dict[categoryName])
            results.append((categoryName, totalRating))
        results = sorted(results, key=lambda x: x[1], reverse=True)
        finalCategories = list(zip(*results))[0][:max_categories]
        print(finalCategories)
        category_l = []
        for categoryName in finalCategories:
            products = [rating.getMappedProduct().getOriginalProduct() for rating in category_predictions_dict[categoryName]]
            category_l.append(Category(categoryName, products))
        return category_l

    @staticmethod
    def getCategoriesForUser(username, max_results=10, fromDB=True):
        ini = time.time()
        results = []
        dbPrediction = None
        if fromDB:
            dbPrediction = MongoHandler.getInstance().getPredictionByUserId(username)
        if dbPrediction:
            results = DBMapper.fromDBResultToPrediction(dbPrediction)
            print("Obtained from DB!")
            return results
        # Calculate them otherwise
        mUser = RecommenderEngine._getMappedUserFromUsername(username)
        if not mUser:
            return
        nn = NN.getInstance()
        category_predictions_dict = dict()
        for nnInputGenerator, categoryName in RecommenderEngine._processCatalogByCategories(mUser):
            predictions = []
            mProducts = []
            for nnInputValue, mProduct in nnInputGenerator():
                prediction = nn.predict(nnInputValue)
                prediction = NNOutput.translatePredictionListToDecimalList(prediction)[0]
                predictions.append(prediction)
                mProducts.append(mProduct)
            predictions = np.array(predictions)
            #mProducts = nnInputSet.getMappedProducts()
            category_predictions_dict[categoryName] = RecommenderEngine._getPredictedCategory(mUser, mProducts, predictions, max_results)
            logger.debug("%s: Finished finding recommendations for category %s" % (username, categoryName))
        fini = time.time()
        results = RecommenderEngine._selectBestCategories(category_predictions_dict)
        return results
