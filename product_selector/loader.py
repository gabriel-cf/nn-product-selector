#!/usr/bin/python2.7
import itertools
from .modules.dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from .modules.dataset_processing.src.model.product import Product
from .modules.dataset_processing.src.model.user import User
from .modules.dataset_processing.src.model.mappeduser import MappedUser
from .modules.dataset_processing.src.model.mappedproduct import MappedProduct
from .modules.dataset_processing.src.mapper.mapper import Mapper
from .modules.dataset_processing.src.model.scenario.rule import Rule

from .modules.keras_learning.nn import NN
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO - Increase when in prod
dMAX = 10

class Loader(object):
    """Class that loads the users, products and Neural Network from the system"""

    ANALYTICS = True
    NN = None
    CACHED_USER_DIC, CACHED_M_USER_DIC = (None, None) # By Nationalities
    CACHED_PRODUCT_DIC, CACHED_M_PRODUCT_DIC = (None, None) # By Categories
    CACHED_RULES_DIC = dict() # [nationality, category]
    @staticmethod
    def getUsersFromDBResult(db_users):
        """ Receives the dictionary result of the query against
            the DB and returns an array of mapped User objects
        """
        logger.info('Processing users from data base results')
        retrievedUsers = []
        i = 0
        for db_user in db_users:
            if (i == dMAX):
                break
            # Retrieve username, gender, age and nationality
            username = db_user['login']['username']
            gender = db_user['gender']
            dateOfBirth = db_user['dob'] #yyyy-mm-dd
            nationality = db_user['nat']
            # Transform string date to date object
            dateOfBirth = datetime.strptime(dateOfBirth.split(' ')[0], '%Y-%m-%d')
            #logger.debug("{};{};{};{}".format(username, gender, dateOfBirth.year, nationality))
            user = User(username, gender, dateOfBirth, nationality)
            retrievedUsers.append(user)
            i+=1
        logger.info('Users processed')

        return retrievedUsers

    @staticmethod
    def getProductsFromDBResult(db_products):
        """ Receives the dictionary result of the query against
             the DB and returns an array of mapped Product objects
        """
        retrievedProducts = []
        i = 0
        for db_product in db_products:
            if (i == dMAX):
                break
            idP = db_product['_id']
            name = db_product['name']
            categories = db_product['sections']
            imageUrl = db_product['image_url']
            if (categories):
                product = Product(idP, name, categories, imageUrl)
                if Loader.ANALYTICS:
                    # Set Ratings
                    db_ratings = MongoHandler.getInstance().getRatingsForProduct(idP)
                    product.setRating([db_rating['_rating'] for db_rating in db_ratings])
                else:
                    product.setRandomRating()
                logger.debug("prod_id:{}, avg_rating:{}".format(product._id, product._avgRating))
                retrievedProducts.append(product)
            i+=1
        logger.info('Products processed')

        return retrievedProducts

    @staticmethod
    def getUsersByNationalityFromDB():
        """ Returns a dictionary holding the users for every nationality
            straight from the query result
        """
        db_nationality_dic = {}
        for nationality_name in Mapper.getAllAvailableNationalities():
            db_nationality_dic[nationality_name] = MongoHandler.getInstance().getUsersByParameters(nationality=nationality_name)

        return db_nationality_dic

    @staticmethod
    def getProductsByCategoryFromDB():
        """ Returns a dictionary holding the products for every category
            straight from the query result
        """
        #i = 0
        db_category_dic = {}
        for category_name in Mapper.getAllAvailableCategories():
            #if (i == 3):
            #    break
            db_category_dic[category_name] = MongoHandler.getInstance().getProductsByParameters(category=category_name)
            #i+=1

        return db_category_dic

    @staticmethod
    def processToMap(old_dic, func):
        new_dic = {}
        for key in old_dic:
            logger.info(key)
            new_dic[key] = func(old_dic[key])
        return new_dic

    @staticmethod
    def processUsersFromDBResult(db_user_dic):
        return Loader.processToMap(db_user_dic, Loader.getUsersFromDBResult)

    @staticmethod
    def processProductsFromDBResult(db_product_dic, analytics=ANALYTICS):
        if analytics != Loader.ANALYTICS:
            Loader.ANALYTICS = not Loader.ANALYTICS
            res = Loader.processToMap(db_product_dic, Loader.getProductsFromDBResult)
            Loader.ANALYTICS = not Loader.ANALYTICS
            return res
        return Loader.processToMap(db_product_dic, Loader.getProductsFromDBResult)

    @staticmethod
    def mapProcessedUsers(processed_user_dic):
        return Loader.processToMap(processed_user_dic, lambda l: [MappedUser(x) for x in l])

    @staticmethod
    def mapProcessedProducts(processed_product_dic):
        return Loader.processToMap(processed_product_dic, lambda l: [MappedProduct(x) for x in l])

    @staticmethod
    def loadUsers():
        if (Loader.CACHED_USER_DIC is None or Loader.CACHED_M_USER_DIC is None):
            logger.info('Loading users from DB')
            # User processing
            db_user_dic = Loader.getUsersByNationalityFromDB()
            logger.info('Processing users from data base results')
            processed_user_dic = Loader.processUsersFromDBResult(db_user_dic)
            mapped_user_dic = Loader.mapProcessedUsers(processed_user_dic)

            Loader.CACHED_USER_DIC = processed_user_dic
            Loader.CACHED_M_USER_DIC = mapped_user_dic # By Nationalities

        return Loader.CACHED_USER_DIC, Loader.CACHED_M_USER_DIC

    @staticmethod
    def loadProducts(analytics=ANALYTICS):
        #if (Loader.CACHED_PRODUCT_DIC is None or Loader.CACHED_M_PRODUCT_DIC is None):
        logger.info('Loading products from DB')
        # Product processing
        db_product_dic = Loader.getProductsByCategoryFromDB()
        logger.info('Processing products from data base results')
        processed_product_dic = Loader.processProductsFromDBResult(db_product_dic, analytics=analytics)
        mapped_product_dic = Loader.mapProcessedProducts(processed_product_dic)
        Loader.CACHED_PRODUCT_DIC = processed_product_dic
        Loader.CACHED_M_PRODUCT_DIC = mapped_product_dic # By Nationalities

        return Loader.CACHED_PRODUCT_DIC, Loader.CACHED_M_PRODUCT_DIC

    @staticmethod
    def loadRules():
        rules = MongoHandler.getInstance().getAllRules()
        for rule in rules:
            Loader.CACHED_RULES_DIC[(Mapper.getNationalityValue(rule['_nationality']),\
            Mapper.getCategoryValue(rule['_category']))]\
            = Rule(rule['_w_age'], rule['_w_male'], rule['_w_female'], rule['_w_avg_rating'], rule['_older_better'])

    @staticmethod
    def loadNN(load_rules=True):
        # Note: specifying rules will train the network with random scenario
        if not Loader.CACHED_RULES_DIC and load_rules:
            Loader.loadRules()
        network = NN.getInstance(rules=Loader.CACHED_RULES_DIC)
        return network

    @staticmethod
    def reloadNN(load_rules=True):
        if not Loader.CACHED_RULES_DIC and load_rules:
            Loader.loadRules()
        NN.trainNewInstance(rules=Loader.CACHED_RULES_DIC)
