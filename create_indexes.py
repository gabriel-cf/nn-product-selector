"""
    This script generates the indexes on the MongoDB
"""


from .a_recommendation.modules.dataset_processing.modules.src.io.mongoconnector.mongohandler import MongoHandler

handler = MongoHandler.getInstance()

if __name__ == '__main__':
    print("Creating indexes for _productId and _userId")
    handler._userDB.users_collection.create_index([('login.username', 1)])
    handler._productDB.products_collection.create_index([('sections', 1)])
    #handler._analysisDB.ratings_collection_mock.create_index([('_productId', 1)])
    #handler._analysisDB.ratings_collection_mock.create_index([('_userId', 1)])
