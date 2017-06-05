#!/usr/bin/python2.7
from pymongo import MongoClient

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MongoHandler(object):
    """ Connection handler between MongoDB and
        user application. Allows queries for users
        and products to the DB
    """
    # Change to False to load real values
    MOCK_ANALYTICS = True
    # Constants for defining connection parameters
    HOST = 'localhost'
    PORT = 27017
    # Constants for defining query parameters
    Q_USER_NATIONALITY = 'nat'
    Q_USER_SEX = 'gender'
    Q_USER_USERNAME = 'login.username'
    Q_PRODUCT_CATEGORY = 'sections'
    Q_PRODUCT_ID = '_id'
    KWARG_NATIONALITY = 'nationality'
    KWARG_SEX = 'sex'
    KWARG_CATEGORY = 'category'
    KWARG_ID = 'id'
    KWARG_USERNAME = 'username'
    INSTANCE = None

    @staticmethod
    def getInstance():
        if (MongoHandler.INSTANCE is None):
            MongoHandler.INSTANCE = MongoHandler()
        return MongoHandler.INSTANCE

    def getAllUsers(self):
        """ Returns all users on the DB"""
        return self._userDB.users_collection.find()
    def getAllProducts(self):
        """ Returns all products on the DB"""
        return self._productDB.products_collection.find().limit(1000)
    def getAllRatings(self, sort=False, maxDate=None):
        res = None
        collection = self._analysisDB.ratings_collection if not MongoHandler.MOCK_ANALYTICS\
         else self._analysisDB.ratings_collection_mock
            #if maxDate: TODO
            #    res = collection.find({"_date": {'$lt': maxDate}})
            #else:
        res = collection.find()
        if sort:
            return res.sort({"_date": -1})
        return res
    def getAllRules(self):
        return self._analysisDB.rules_collection_mock.find()
    def getRatingsForProduct(self, productId, maxDate=None):
        """ Returns all ratings on the DB"""
        if maxDate:
            query = {"_productId": productId, "_date": {'$lt': maxDate}}
        else:
            query = {"_productId": productId}
        if MongoHandler.MOCK_ANALYTICS:
            return self._analysisDB.ratings_collection_mock.find(query)
        return self._analysisDB.ratings_collection.find(query)

    def getRuleForNationalityAndCategory(self, nationality, category):
        # Note: it can only be in mock
        query = {"_nationality":nationality, "_category":category}
        return self._analysisDB.rules_collection_mock.find_one(query)

    def getUsersByParameters(self, one_only=False, **parameters):
        query_parameters = {}
        # Check user parameters and create new dic with query parameters names
        for key in parameters:
            if (key == MongoHandler.KWARG_NATIONALITY):
                query_parameters[MongoHandler.Q_USER_NATIONALITY] = parameters[MongoHandler.KWARG_NATIONALITY]
            elif (key == MongoHandler.KWARG_SEX):
                query_parameters[MongoHandler.Q_USER_SEX] = parameters[MongoHandler.KWARG_SEX]
            elif (key == MongoHandler.KWARG_USERNAME):
                query_parameters[MongoHandler.Q_USER_USERNAME] = parameters[MongoHandler.KWARG_USERNAME]
            else:
                raise ValueError("Parameter '%s' is not a valid user query one" % (key))
        # Return results
        if one_only:
            return self._userDB.users_collection.find_one(query_parameters)
        return self._userDB.users_collection.find(query_parameters)

    def getProductsByParameters(self, one_only=False, **parameters):
        query_parameters = {}
        # Check user parameters and create new dic with query parameters names
        for key in parameters:
            if (key == MongoHandler.KWARG_CATEGORY):
                query_parameters[MongoHandler.Q_PRODUCT_CATEGORY] = parameters[MongoHandler.KWARG_CATEGORY]
            elif (key == MongoHandler.KWARG_ID):
                query_parameters[MongoHandler.Q_PRODUCT_ID] = parameters[MongoHandler.KWARG_ID]
            else:
                raise ValueError("Parameter '%s' is not a valid product query one" % (key))
        # Return results
        if one_only:
            return self._productDB.products_collection.find_one(query_parameters)
        return self._productDB.products_collection.find(query_parameters)

    def getProductById(self, productId):
        return self._productDB.products_collection.find_one({'_id': productId})

    def __init__(self):
        logging.info("Attempting connection with MongoDB service")
        self._client = MongoClient(MongoHandler.HOST, MongoHandler.PORT) # Generate client and connect to service
        logging.info("Connection established with MongoDB service")
        self._userDB = self._client.tfg_users # Access point to Users DB
        self._productDB = self._client.amazon_products # Access point to Amazon Products DB
        self._analysisDB = self._client.analysis # Access point to Amazon Products DB
