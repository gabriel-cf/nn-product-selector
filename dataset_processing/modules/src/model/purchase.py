from datetime import date, datetime
from user import User
from product import Product
from numbers import Number

class Purchase(object):
	""" Purchase object for storing data related to a purchase of a product """
	def __init__(self, user, product, purchase_date, rating):
		""" user : User
			product : Product
			purchase_date : Date
			rating : Float (can be None)
		"""
		if (type(user) is User):
			self._user = user
		else:
			raise ValueError('user attribute must be of type User')
		if (type(product) is Product):
			self._product = product
		else:
			raise ValueError('product attribute must be of type Product')
		if (type(purchase_date) is Date):
			self._purchase_date = purchase_date
		else:
			raise ValueError('purchase_date attribute must be of type Date')
		if (isinstance(rating, Number) or (rating is None)):
			self._rating = rating	
		else:
			raise ValueError('rating attribute must be of type Number or None')
		
