import logging
import time
from ...dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBUpdateRates(object):
    """Updates the 'rate' field of the products inside productDB.products_collection
       as the average value of the ratings inside analysisDB.ratings_collection.
       Note: in mock mode, it will be the ratings from analysisDB.ratings_collection_mock.
    """
    @staticmethod
    def job():
        handler = MongoHandler.getInstance()
        pipeline = [
            {"$group":
                {
                    "_id": {"user": "$_userId", "product": "$_productId"},
                    "totalSum": {"$sum": "$_productRating"},
                    "avgSum": {"$avg": "$_productRating"},
                    "count": {"$sum": 1}
                }
            }
        ]
        i = 0
        ini = time.time()
        for product_rating in handler._analysisDB.ratings_collection_mock.aggregate(pipeline):
            _id = product_rating['_id']['product']
            avgSum = product_rating['avgSum']
            handler._productDB.products_collection.update_one({
              '_id': _id
            },{
              '$set': {
                'rate': avgSum
              }
            }, upsert=False)
            i += 1
            if(i%1000==0):
                logger.info("Updated: %d product average ratings" % i)
        fini = time.time()
        logger.info("Updated: %d product average ratings" % i)
        logger.info("Completed in: %ds" % (fini - ini))
