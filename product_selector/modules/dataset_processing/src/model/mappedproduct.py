from ..mapper.mapper import Mapper

class MappedProduct(object):
	def __init__(self, product):
		self._product = product
		self._mainCategory = Mapper.getCategoryValue(product._mainCategory)
		self._avgRating = product._avgRating

	def hasCategory(self):
		return not self._mainCategory is None

	def getOriginalProduct(self):
		return self._product
