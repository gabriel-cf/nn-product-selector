import json
import csv

class Category(object):
	"""Product ready to be serialized as JSON and sent to the client"""
	def __init__(self, categoryType):
		super(Category, self).__init__()
		self._categoryType = categoryType

		

class CategoryEncoder(json.JSONEncoder):
	def default(self, obj):
		#if not isinstance(obj, ProductList):
		#	return super(ProductList, self).default(obj)

		return obj.__dict__

with open("general_product_categories.csv", 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';')
	for row in spamreader:
		for categoryName in row:
			print json.dumps(Category(categoryName), cls=CategoryEncoder)

	
