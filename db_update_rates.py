import time
from .product_selector.modules.dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler

if __name__ == '__main__':
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
        username = product_rating['_id']['user']
        avgSum = product_rating['avgSum']
        productBefore = handler._productDB.products_collection.find_one({"_id": _id})
        handler._productDB.products_collection.update_one({
          '_id': _id
        },{
          '$set': {
            'rate': avgSum
          }
        }, upsert=False)
        print("%f:%s" % (avgSum, _id))
        i += 1
        if(i%1000==0):
            print("Completed: %d" % i)
    fini = time.time()
    print("Completed: %d" % i)
    print("Completed in: %ds" % (fini - ini))
