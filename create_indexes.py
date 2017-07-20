"""
    This script generates the indexes on the MongoDB
"""


from .product_selector.modules.dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler

handler = MongoHandler.getInstance()

if __name__ == '__main__':
    print("Creating indexes for _productId and _userId")
    #handler._userDB.users_collection.create_index([('login.username', 1)])
    handler._productDB.products_collection.drop_indexes()
    handler._productDB.products_collection.create_index([('mainCategory', 1)])
    handler._productDB.products_collection.create_index([('_id', 1)])
    #handler._analysisDB.ratings_collection_mock.create_index([('_productId', 1)])
    #handler._analysisDB.ratings_collection_mock.create_index([('_userId', 1)])
