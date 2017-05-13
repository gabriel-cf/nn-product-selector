from .product import Product

class Category(object):
	"""Category object holding the list of recommended products"""
	def __init__(self, name, l_products):
		self._categoryName = name
		self._productList = l_products
