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
			rating : Float (can be null)
		"""
		self._user = user if (type(user) is User) else raise ValueError('user attribute must be of type User')
		self._product = product if (type(product) is Product) else ValueError('product attribute must be of type Product')
		self._purchase_date = purchase_date if (type(purchase_date) is Date) else ValueError('purchase_date attribute must be of type Date')
		self._rating = rating if (isinstance(rating, Number)) else None
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
			rating : Float (can be null)
		"""
		self._user = user if (type(user) is User) else raise ValueError('user attribute must be of type User')
		self._product = product if (type(product) is Product) else ValueError('product attribute must be of type Product')
		self._purchase_date = purchase_date if (type(purchase_date) is Date) else ValueError('purchase_date attribute must be of type Date')
		self._rating = rating if (isinstance(rating, Number)) else None
		
