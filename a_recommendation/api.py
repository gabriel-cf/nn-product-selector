#!/usr/bin/python2.7
from .modules.dataset_processing.modules.src.io.mongoconnector.mongohandler import MongoHandler
from .modules.dataset_processing.modules.src.model.mappeduser import MappedUser
from .modules.dataset_processing.modules.src.model.category import Category
from .modules.dataset_processing.modules.src.model.recommendation import Recommendation
from .modules.dataset_processing.modules.src.mapper.mapper import Mapper
from .modules.dataset_processing.modules.src.io.response.recommendationresponse import RecommendationResponse
from .loader import Loader
from .modules.batch.scheduler import Scheduler

from .modules.keras_learning.io.nninput import NNInput
from .modules.keras_learning.io.nnoutput import NNOutput
from .modules.keras_learning.nn import NN
import numpy as np
import itertools

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def getRecommendationsByCategory(m_user, max_results=5):
    category_recommendations = {}
    for category in CACHED_M_PRODUCT_DIC:
        m_category = Mapper.getCategoryValue(category)
        rule = NN.getRule(m_user._nationality, m_category)
        logger.info("Using rule: %r", rule)
        # Cartesian product of Nationalities and Categories
        combinations = itertools.product([m_user], CACHED_M_PRODUCT_DIC[category])

        recommendations = []
        inputSet = NNInput.getNNInputList(combinations)
        logger.info('Getting predictions')
        predictions = NNOutput.translatePredictionListToDecimalList(NN.predict(inputSet))
        # Get the indexes of the highest values
        logger.debug(predictions)
        max_results = len(predictions) if max_results > len(predictions) else max_results
        ind = np.argpartition(predictions, -max_results)[-max_results:]
        ind = ind[np.argsort(predictions[ind])[::-1]]
        for i in ind:
            m_product = CACHED_M_PRODUCT_DIC[category][i]
            product = CACHED_PRODUCT_DIC[category][i]
            nn_prediction = predictions[i]
            rule_prediction = rule.getEstimatedLikeValue(m_user, m_product)
            logger.info("\033[32mRULE Like: %.6f%%\033[0m", rule_prediction * 100)
            logger.info("User: Nationality=%s;Gender=%s;Age=%s Product: Category=%s;Avg Rating=%s", m_user._nationality, m_user._gender, m_user._age, m_product._mainCategory, m_product._avgRating)
            logger.info("\033[32mNN Like: %.6f%%\033[0m", nn_prediction * 100)
            logger.info("\033[33mDiff = %.6f%%\033[0m", (rule_prediction - nn_prediction) * 100)
            logger.info("------------------------")
            recommendations.append(product)
        category_recommendations[category] = recommendations

    return category_recommendations

def getRecommendationResponseJSON(username):
    """    Receives a dictionary with the recommended categories and products
        and generates the JSON
    """
    user_db = MongoHandler.getInstance().getUsersByParameters(one_only=True, username=username)
    if (user_db is None):
        logger.warning("No users were found for username '%s'" % username)
        return None
    user = Loader.getUsersFromDBResult([user_db])[0]
    category_recommendations = getRecommendationsByCategory(MappedUser(user))
    category_l = []
    for category_name in category_recommendations:
        category_l.append(Category(category_name, category_recommendations[category_name]))
    recommendation = Recommendation(category_l)

    json_o = RecommendationResponse.getJSON(recommendation)
    logger.debug(json_o)

    return json_o

NN = Loader.loadNN()
CACHED_USER_DIC, CACHED_M_USER_DIC = Loader.loadUsers() # By Nationalities
CACHED_PRODUCT_DIC, CACHED_M_PRODUCT_DIC = Loader.loadProducts(analytics=False) # By Categories
loadProductsJob = (Loader.loadProducts, 3)
ReloadNNJob = (Loader.reloadNN, 24)
scheduler = Scheduler([loadProductsJob, ReloadNNJob])
scheduler.start()
#CACHED_RATING_DIC, CACHED_M_RATING_DIC = Loader.loadRatings() # By Categories
#CACHED_SALES_DIC, CACHED_M_SALES_DIC = Loader.loadSales() # By Categories

if __name__ == '__main__':
    # Test
    user = CACHED_USER_DIC['ES'][0]
    json_s = getRecommendationResponseJSON(user._username)
