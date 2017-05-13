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
	# Constants for defining connection parameters
	HOST = 'localhost'
	PORT = 27017
	# Constants for defining query parameters
	Q_USER_NATIONALITY = 'nat'
	Q_USER_SEX = 'gender'
	Q_USER_USERNAME = 'login.username'
	Q_PRODUCT_CATEGORY = 'sections'
	KWARG_NATIONALITY = 'nationality'
	KWARG_SEX = 'sex'
	KWARG_CATEGORY = 'category'
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
		return self._productDB.products_collection.find()

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

	def getProductsByParameters(self, **parameters):
		query_parameters = {}
		# Check user parameters and create new dic with query parameters names
		for key in parameters:
			if (key == MongoHandler.KWARG_CATEGORY):
				query_parameters[MongoHandler.Q_PRODUCT_CATEGORY] = parameters[MongoHandler.KWARG_CATEGORY]
			else:
				raise ValueError("Parameter '%s' is not a valid product query one" % (key))
		# Return results
		return self._productDB.products_collection.find(query_parameters)
	
	def __init__(self):
		logging.info("Attempting connection with MongoDB service")
		self._client = MongoClient(MongoHandler.HOST, MongoHandler.PORT) # Generate client and connect to service
		logging.info("Connection established with MongoDB service")
		self._userDB = self._client.tfg_users # Access point to Users DB 
		self._productDB = self._client.amazon_products # Access point to Amazon Products DB

