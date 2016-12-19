class Product(object):

	def addToPurchases(self, purchase):
		if (type(purchase) is Purchase):
			self._purchases.append(purchase)
		else:
			ValueError('purchase object must be of type Purchase')

	def __init__(self, prodID, name, categories, imageURL):
		self._id = prodID
		self._name = name
		self._categories = categories		
		self._mainCategory = categories[0]

