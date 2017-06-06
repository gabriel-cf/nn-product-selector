import logging
from ...dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ...recommender_engine.recommender_engine import RecommenderEngine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBUpdatePredictions(object):
    """docstring for ."""
    @staticmethod
    def job():
        i = 0
        handler = MongoHandler.getInstance()
        dbUsers = handler.getAllUsers()
        for dbUser in dbUsers:
            if i % 5 == 0:
                logger.info("Processed %d users" % i)
                username = dbUser['login']['username']
                categories = RecommenderEngine.getCategoriesForUser(username, fromDB=False)
                if categories and len(categories) > 0:
                    predictions = []
                    docSavedPrediction = {
                        '_userId': username,
                        '_predictions': predictions
                    }
                    for category in categories:
                        product_l = category.getProductList()
                        if product_l and len(product_l) > 0:
                            products = [product.getId() for product in product_l]
                            category = {category.getCategoryName(): products}
                            predictions.append(category)
                            handler._analysisDB.predictions_collection.update_one({
                            '_userId': username
                            },{
                            '$set': {
                            '_predictions': predictions
                            }
                            }, upsert=True)
                            logger.info("Inserted predictions for user %s" % username)
                            #handler._analysisDB.ratings_collection_mock.insert_one(docRating)
                            i += 1
