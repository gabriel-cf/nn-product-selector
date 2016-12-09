#!/usr/bin/python2.7

import os, sys
sys.path.append(os.path.join('..', '..', 'io', 'mongoconnector'))
sys.path.append(os.path.join('..', '..', 'model'))

from mongohandler import MongoHandler
from product import Product
from user import User
from mappeduser import MappedUser
from mappedproduct import MappedProduct
from datetime import date, datetime

def getUsersFromDBResult(db_users):
	""" Receives the dictionary result of the query against
	 	the DB and returns an array of mapped User objects
	"""
	retrievedUsers = []
	for db_user in db_users:
		# Retrieve username, gender, age and nationality
		username = db_user['login']['username']
		gender = db_user['gender']
		dateOfBirth = db_user['dob'] #yyyy-mm-dd
		nationality = db_user['nat']
		# Transform string date to date object
		dateOfBirth = datetime.strptime(dateOfBirth.split(' ')[0], '%Y-%m-%d')
		#print("{};{};{};{}".format(username, gender, dateOfBirth.year, nationality))
		user = User(username, gender, dateOfBirth, nationality)
		retrievedUsers.append(user)

	return retrievedUsers

def getProductsFromDBResult(db_products):
	""" Receives the dictionary result of the query against
	 	the DB and returns an array of mapped Product objects
	"""
	retrievedProducts = []
	for db_product in db_products:
		idP = db_product['_id']
		name = db_product['name']
		categories = db_product['sections']
		imageUrl = db_product['image_url']
		if (categories):
			product = Product(idP, name, categories, imageUrl)
			retrievedProducts.append(product)

	return retrievedProducts

if __name__ == '__main__':
	mongoHandler = MongoHandler()

	db_users = mongoHandler.getUsersFromDB()
	users = getUsersFromDBResult(db_users)
	mappedUsers = []

	for user in users:
		mappedUsers.append(MappedUser(user))

	db_products = mongoHandler.getProductsFromDB()
	products = getProductsFromDBResult(db_products)
	mappedProducts = []

	for product in products:
		print "{} --> {}".format(product._mainCategory, MappedProduct(product)._mainCategory)
		mappedProducts.append(MappedProduct(product))




