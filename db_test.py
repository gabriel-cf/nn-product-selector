from .a_recommendation.modules.dataset_processing.modules.src.io.mongoconnector.mongohandler import MongoHandler

if __name__ == '__main__':
    handler = MongoHandler.getInstance()
    print(handler._productDB.products_collection.find_one())
    print(handler._productDB.products_collection.find().count())
    print("#################################################")
    print(handler._userDB.users_collection.find_one())
    print(handler._userDB.users_collection.find().count())
    print("#################################################")
    print(handler._analysisDB.rules_collection_mock.find_one())
    print(handler._analysisDB.rules_collection_mock.find().count())
    print("--------------------------------------------------")
    print(handler._analysisDB.sales_collection_mock.find_one())
    print(handler._analysisDB.sales_collection_mock.find().count())
