from ...dataset_processing.src.model.mappedproduct import MappedProduct
from ...dataset_processing.src.model.mappeduser import MappedUser

import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNInput(object):
	""" An object that translates values from a mapped user
		and a product into a format understandable by the NN
	"""
	@staticmethod
	def getNNInput(mapped_user, mapped_product, only_entry=False):
		""" mapped_user --> MappedUser object
		 	mapped_product --> MappedProduct object
		 	only_entry (default=False) --> Return only the input entry of the numpy array
			returns --> NNInput object holding the value required by the NN
		"""
		if (not isinstance(mapped_user, MappedUser) or mapped_user is None):
			raise TypeError('mapped_user object must be of type MappedUser')
		if (not isinstance(mapped_product, MappedProduct) or mapped_product is None):
			raise TypeError('mapped_product object must be of type MappedProduct')
		input_entry = [
			float(mapped_user._nationality),
			float(mapped_user._gender),
			float(mapped_user._age),
			float(mapped_product._mainCategory),
			float(mapped_product._avgRating)
			]
		if only_entry:
			return input_entry
		t_X = np.array([input_entry])
		return t_X

	@staticmethod
	def getNNInputList(mapped_user_product_tuple_list):
		""" Takes a list of tuples (mapped_user, mapped_product)
			and returns a list of inputs ready to be processed by the NN
		"""
		t_X = []
		for user, product in mapped_user_product_tuple_list:
			t_X.append(NNInput.getNNInput(user, product, only_entry=True))
		return np.array(t_X)

	def __init__(self, mapped_user, mapped_product):
		self._value = NNInput.getNNInput(mapped_user, mapped_product)
