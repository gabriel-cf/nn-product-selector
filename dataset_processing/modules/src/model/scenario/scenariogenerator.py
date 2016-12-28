from __future__ import division
import itertools
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ...mapper.mapper import Mapper
from ..user import User
from ..product import Product
from ..mappeduser import MappedUser
from ..mappedproduct import MappedProduct
from ..enum.sexenum import Sex
from ......keras_learning.nn import NNTrainingInputSet
from rule import Rule
from rulegenerator import RuleGenerator

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ScenarioGenerator:
	""" A generator of random scenarios for users and products
		An scenario is the combination of user nationalities with
		product categories, where for each one a generated rule determines
		the estimated like according to user and product factors.

		This generates training data using dummy users and products.
		The final result is a TrainingInputSet ready to be set in the NN
	"""
	ALL_NATIONALITIES = Mapper.getAllAvailableNationalities()
	ALL_CATEGORIES = Mapper.getAllAvailableCategories()
	MAX_DUMMY_USERS = 10
	MAX_DUMMY_PRODUCTS = 50
	MIN_AGE = 16
	MAX_AGE = 100
	AGE_GAP = (MAX_AGE - MIN_AGE) // MAX_DUMMY_USERS

	@staticmethod
	def getDummyUser(nationality, index, male=True):
		gender = Sex.MALE if male else Sex.FEMALE
		name = "".join(["dummy_user_", "%i" % index, "_", gender])
		age = datetime.now() - relativedelta(years=(ScenarioGenerator.MIN_AGE + index * ScenarioGenerator.AGE_GAP))
		nationality = nationality
		user = User(name, gender, age, nationality)
		return user

	@staticmethod
	def getDummyProduct(category, index):
		prodID = 1
		name = "".join(["dummy_product_", "%i" % index])
		categories = [category]
		imageURL = ""
		avgRating = index / 10 # 0.0, 0.1, .. 5.0
		product = Product(prodID, name, categories, imageURL, avgRating)
		return product

	@staticmethod
	def getDummyUsersProductsRule():
		combinations = itertools.product(ScenarioGenerator.ALL_NATIONALITIES, ScenarioGenerator.ALL_CATEGORIES) # Cartesian product of Nationalities and Categories
		dummy_combinations = [] # --> [(dummyusers0x0, dummyproducts0x0, rule0x0), (dummyusers0x1, dummyproducts0x1, rule0x1) .. , ((natnxcatk dummyusers, natnxcatk dummyproducts))]
		for nationality, category in combinations:
			# Generate rule
			rule = RuleGenerator.generateRule()
			# Generate dummy users
			dummy_user_l = []
			for sex in xrange(0,2):
				for i in xrange(0, ScenarioGenerator.MAX_DUMMY_USERS + 1):
					dummy_user_l.append(ScenarioGenerator.getDummyUser(nationality, i, male=(sex==0)))
			# Generate dummy products
			dummy_product_l = []
			for i in xrange(0, ScenarioGenerator.MAX_DUMMY_PRODUCTS + 1):
				dummy_product_l.append(ScenarioGenerator.getDummyProduct(category, i))

			dummy_combinations.append((dummy_user_l, dummy_product_l, rule))
		return dummy_combinations

	@staticmethod
	def generateTrainingInputSet():
		dummy_combinations = ScenarioGenerator.getDummyUsersProductsRule()
		nnTrainingInputSet = NNTrainingInputSet()
		# For each combination of users and products under a given rule
		no_combinations = len(dummy_combinations)
		i = 0
		for users, products, rule in dummy_combinations:
			# Combine every user with all products
			combinations = itertools.product(users, products)
			for user, product in combinations:
				sex = user._gender
				expected_like = rule.getEstimatedLikeValue(user._age, user._gender, product._avgRating)
				nnTrainingInputSet.addToTrainingInput(MappedUser(user), MappedProduct(product), expected_like)
			i += 1
			logger.info("Finished combination %s of %s" % (i, no_combinations))

		return nnTrainingInputSet



