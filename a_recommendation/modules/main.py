#!/usr/bin/python2.7
from dataset_processing.modules.src.io.mongoconnector.mongohandler import MongoHandler
from dataset_processing.modules.src.model.enum.sexenum import Sex
from dataset_processing.modules.src.model.product import Product
from dataset_processing.modules.src.model.user import User
from dataset_processing.modules.src.model.mappeduser import MappedUser
from dataset_processing.modules.src.model.mappedproduct import MappedProduct
from dataset_processing.modules.src.model.scenario.scenariogenerator import ScenarioGenerator
from dataset_processing.modules.src.model.scenario.rulegenerator import RuleGenerator
from dataset_processing.modules.src.model.scenario.rule import Rule
from dataset_processing.modules.src.mapper.mapper import Mapper

from keras_learning.nn import NN, NNInput, NNOutput
from datetime import date, datetime
from random import randint
import numpy as np
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dMAX = 20

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
			retrievedProducts.append(product)
		i+=1

		#logger.debug("{};{};{}".format(product._id, product._name, product._mainCategory))


	logger.info('Products processed')
	return retrievedProducts

def getUsersByNationalityFromDB(mongohandler):
	""" Returns a dictionary holding the users for every nationality
		straight from the query result
	"""
	db_nationality_dic = {}
	for nationality_name in Mapper.getAllAvailableNationalities():
		db_nationality_dic[nationality_name] = mongohandler.getUsersByParameters(nationality=nationality_name)

	return db_nationality_dic

def getProductsByCategoryFromDB(mongohandler):
	""" Returns a dictionary holding the products for every category
		straight from the query result
	"""
	i = 0
	db_category_dic = {}
	for category_name in Mapper.getAllAvailableCategories():
		if (i == 2):
			break
		db_category_dic[category_name] = mongohandler.getProductsByParameters(category=category_name)
		i+=1

	return db_category_dic

def mapUsers(processed_user_l):
	return map(lambda x: MappedUser(x), processed_user_l)

def mapProducts(processed_product_l):
	return map(lambda x: MappedProduct(x), processed_product_l)

def processToMap(old_dic, func):
	new_dic = {}
	for key in old_dic:
		new_dic[key] = func(old_dic[key])
	return new_dic

def processUsersFromDBResult(db_user_dic):
	return processToMap(db_user_dic, getUsersFromDBResult)

def mapProcessedUsers(processed_user_dic):
	return processToMap(processed_user_dic, mapUsers)

def processProductsFromDBResult(db_product_dic):
	return processToMap(db_product_dic, getProductsFromDBResult)

def mapProcessedProducts(processed_product_dic):
	return processToMap(processed_product_dic, mapProducts)


if __name__ == '__main__':
	logger.info('Generating random scenario')
	nnTrainingInputSet, rule_dic = ScenarioGenerator.generateTrainingInputSet()

	logger.info('Executing Neural Input Generator')
	logger.info('Loading Neural Network')
	network = NN.getInstance(loadDataFromDefaultFile=False)
	logger.info('Setting Training Input')
	network.setTrainingInput(nnTrainingInputSet)
	logger.info('Training Network')
	network.trainModel()

	logger.info('Establishing connection with DB')
	mongoHandler = MongoHandler()
	logger.info('Retrieving users from DB')
	# User processing
	db_user_dic = getUsersByNationalityFromDB(mongoHandler) #mongoHandler.getAllUsers()
	logger.info('Processing users from data base results')
	processed_user_dic = processUsersFromDBResult(db_user_dic)
	mapped_user_dic = mapProcessedUsers(processed_user_dic)

	# Product processing
	db_product_dic = getProductsByCategoryFromDB(mongoHandler) #mongoHandler.getAllUsers()
	logger.info('Processing products from data base results')
	processed_product_dic = processProductsFromDBResult(db_product_dic)
	mapped_product_dic = mapProcessedProducts(processed_product_dic)

	users = getUsersFromDBResult(db_user_dic['ES'])
	mappedUsers = []
	logger.info('Mapping users')
	for user in users:
		mUser = MappedUser(user)
		mappedUsers.append(mUser)
		logger.debug("Gender={};Nationality={};Age={}".format(user._gender, user._nationality, user._age))
		logger.debug("\033[32mGenderM={};NationalityM={};AgeM={}\033[0m".format(mUser._gender, mUser._nationality, mUser._age))
	logger.info('Users mapped')

	logger.info('Retrieving products from DB')
	db_products = mongoHandler.getAllProducts()
	products = getProductsFromDBResult(db_products)
	mappedProducts = []

	logger.info('Mapping products')
	for product in products:
		#logger.debug("{} --> {}".format(product._mainCategory, MappedProduct(product)._mainCategory))
		mProduct = MappedProduct(product)
		mProduct._avgRating = float(randint(0,5))
		mappedProducts.append(mProduct)
		logger.debug("Main Category={};Avg Rating={};No. Purchases={}".format(product._mainCategory, product._avgRating, product._noPurchases))
		logger.debug("\033[32mMain CategoryM={};Avg RatingM={};No. PurchasesM={}\033[0m".format(mProduct._mainCategory, mProduct._avgRating, mProduct._noPurchases))
	logger.info('Products mapped')

	
	logger.info('zipping lists')
	mapped_user_product_list = zip(mappedUsers, mappedProducts)

	logger.info('Creating NNInput list')
	inputSet = NNInput.getNNInputList(mapped_user_product_list)
	logger.info('Getting predictions')
	predictions = network.predict(inputSet)
	i = 0
	xAxis = np.array(range(0, len(mapped_user_product_list)))
	nPredictionPlot = []
	rPredictionPlot = []
	for user, product in mapped_user_product_list:
		rule = rule_dic[(user._nationality, product._mainCategory)]
		if (i == 0):
			logger.info("Using rule: %r" % rule)
		
		rule_prediction = rule.getEstimatedLikeValue(user, product)
		nn_prediction = NNOutput.translatePredictionToDecimal(predictions[i])
		logger.debug("User: Nationality={};Gender={};Age={} Product: Category={};Avg Rating={}".format(user._nationality, user._gender, user._age, product._mainCategory, product._avgRating))
		logger.info("\033[32mRULE Like: %.6f%%\033[0m" % (rule_prediction * 100))
		logger.info("\033[32mNN Like: %.6f%%\033[0m" % (nn_prediction * 100))		
		logger.info("\033[33mDiff = %.6f%%\033[0m" % ((rule_prediction - nn_prediction) * 100))
		logger.info("------------------------")
		rPredictionPlot.append(rule_prediction)
		nPredictionPlot.append(nn_prediction)
		i = i + 1
	nPredictionPlot = np.array(nPredictionPlot)
	rPredictionPlot = np.array(rPredictionPlot)
	plt.plot(xAxis,nPredictionPlot,'bs',xAxis,rPredictionPlot,'r^')
	plt.ylabel('NN and Rule predictions')
	plt.show()
