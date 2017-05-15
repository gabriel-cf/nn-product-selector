from __future__ import division
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

	def __init__(self, prodID, name, categories, imageURL, avgRating = 0.0):
		self._id = prodID
		self._name = name
		self._categories = categories
		self._mainCategory = categories[0]
		self._avgRating = avgRating
		self._noRatings = 0
		self._imageURL = imageURL
