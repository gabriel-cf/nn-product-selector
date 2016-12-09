import os, sys
sys.path.append(os.path.join('..', 'mapper'))

import mapper
from mapper import Mapper

class MappedProduct(object):
	def __init__(self, product):
		self._mainCategory = Mapper.getCategoryValue(product._mainCategory)

