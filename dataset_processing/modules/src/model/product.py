class Product(object):
	
	def updateRating(self, new_rate):
		self._avgRating = (self._avgRating * noPurchases + new_rate) / (noPurchases + 1)

	def __init__(self, prodID, name, categories, imageURL, avgRating = 0.0, noPurchases = 0):
		self._id = prodID
		self._name = name
		self._categories = categories		
		self._mainCategory = categories[0]
		self._avgRating = avgRating
		self._noPurchases = noPurchases

