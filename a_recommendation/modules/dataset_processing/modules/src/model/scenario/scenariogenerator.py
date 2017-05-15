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
from ......keras_learning.io.nntraininginputset import NNTrainingInputSet
from rule import Rule
from rulegenerator import RuleGenerator

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ScenarioGenerator:
	""" A generator of random scenarios for users and products
		A scenario is the combination of user nationalities with
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
	def getDummyUsersProductsRule(rules=None):
		combinations = itertools.product(ScenarioGenerator.ALL_NATIONALITIES, ScenarioGenerator.ALL_CATEGORIES) # Cartesian product of Nationalities and Categories
		dummy_combinations = [] # --> [(dummyusers0x0, dummyproducts0x0, rule0x0), (dummyusers0x1, dummyproducts0x1, rule0x1) .. , ((natnxcatk dummyusers, natnxcatk dummyproducts))]
		for nationality, category in combinations:
			rule = None
			if not rules:
				# Generate rule
				rule = RuleGenerator.generateRule()
			else:
				print nationality
				print Mapper.getNationalityValue(nationality)
				print category
				print Mapper.getCategoryValue(category)
				rule = rules[(Mapper.getNationalityValue(nationality), Mapper.getCategoryValue(category))]
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
	def generateTrainingInputSet(rules=None):
		dummy_combinations = ScenarioGenerator.getDummyUsersProductsRule(rules=rules)
		nnTrainingInputSet = NNTrainingInputSet()
		# For each combination of users and products under a given rule
		no_combinations = len(dummy_combinations)
		rule_dic = {}

		i = 0
		for users, products, rule in dummy_combinations:
			# Map rule for the given combination nationalityXcategory
			if not rules:
				rule_dic[(MappedUser(users[0])._nationality, MappedProduct(products[0])._mainCategory)] = rule
			# Combine every user with all products
			combinations = itertools.product(users, products)
			for user, product in combinations:
				mapped_user = MappedUser(user)
				mapped_product = MappedProduct(product)
				expected_like = rule.getEstimatedLikeValue(mapped_user, mapped_product)
				nnTrainingInputSet.addToTrainingInput(mapped_user, mapped_product, expected_like)
			i += 1
			logger.info("Finished combination %s of %s" % (i, no_combinations))
		nnTrainingInputSet._rule_dic = rules
		return nnTrainingInputSet
