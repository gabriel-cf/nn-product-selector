class Product(object):
	def __init__(self, prodID, name, categories, imageURL):
		self._id = prodID
		self._name = name
		self._categories = categories		
		self._mainCategory = categories[0]

