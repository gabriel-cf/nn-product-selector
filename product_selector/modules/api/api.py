import logging
from ..dataset_processing.src.model.recommendation import Recommendation
from ..dataset_processing.src.io.response.recommendationresponse import RecommendationResponse
from ..recommender_engine.recommender_engine import RecommenderEngine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def getRecommendationResponseJSON(username):
    """ Return categories for the given username"""
    category_l = RecommenderEngine.getCategoriesForUser(username)
    if not category_l:
        return None
    recommendation = Recommendation(category_l)
    json_o = RecommendationResponse.getJSON(recommendation)
    logger.debug(json_o)

    return json_o
