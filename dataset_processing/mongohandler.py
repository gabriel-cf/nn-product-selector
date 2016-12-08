#!/usr/bin/python2.7
from pymongo import MongoClient

class MongoHandler(object):
	""" Connection handler between MongoDB and
		user application. Allows queries for users
		and products to the DB
	"""
	# Constants to define connection parameters
	HOST = 'localhost'
	PORT = 27017

	def getUsersFromDB(self):
		""" Returns all users on the DB"""
		return self._userDB.users_collection.find()
	def getProductsFromDB(self):
		""" Returns all products on the DB"""
		return self._productDB.products_collection.find()

	def __init__(self):
		self._client = MongoClient(MongoHandler.HOST, MongoHandler.PORT) # Generate client and connect to service
		self._userDB = self._client.tfg_users # Access point to Users DB 
		self._productDB = self._client.amazon_products # Access point to Amazon Products DB
