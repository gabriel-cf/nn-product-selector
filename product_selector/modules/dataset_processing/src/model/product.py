
from random import uniform

class Product(object):

	def updateRating(self, new_rate):
		self._avgRating = (self._avgRating * self._noRatings + new_rate) / (self._noRatings + 1)
		self._noRatings += 1

	def setRandomRating(self):
		self._avgRating = uniform(0,5)

	def setRating(self, ratingList):
		self._noRatings = max(len(ratingList), 1)
		self._avgRating = sum(ratingList) / self._noRatings

	def getCategory(self):
		return self._mainCategory

	def hasCategory(self):
		return not self._mainCategory is None and not self._mainCategory == 'None'

	def getId(self):
		return self._id

	def __init__(self, prodID, name, mainCategory, imageURL, avgRating = 0.0):
		self._id = prodID
		self._name = name
		self._mainCategory = mainCategory
		self._avgRating = avgRating
		self._noRatings = 0
		self._imageURL = imageURL
