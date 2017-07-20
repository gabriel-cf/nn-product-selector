from ...dataset_processing.src.model.mappedproduct import MappedProduct
from ...dataset_processing.src.model.mappeduser import MappedUser

from numbers import Number
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNOutput(object):
	""" An object that translates a list of decimal output values into
		a format understandable by the NN
	"""
	MAX_VALUE = 5.0

	@staticmethod
	def getNNValues(outputValue, only_entry=False):
		""" outputValue --> decimal value within [0, NNOutput.MAX_VALUE]
			returns --> numpy matrix where each row is an expected output
		"""
		if (not isinstance(outputValue, Number) or outputValue is None):
			raise TypeError('outputValue must be of type Number')
		# Normalize value between [0, NNOutput.MAX_VALUE]
		if (outputValue > NNOutput.MAX_VALUE):
			outputValue = 1.0
		elif (outputValue > 1.0):
			outputValue = outputValue / 5
		entry = [float(outputValue)]
		if only_entry:
			return entry
		t_Y = np.array([entry])
		return t_Y

	@staticmethod
	def translatePredictionToDecimal(nnOutputValue):
		if (nnOutputValue is None):
			raise ValueError('nnOutputValue must have a decimal value non None')
		return nnOutputValue[0]

	@staticmethod
	def translatePredictionListToDecimalList(nnOutputValue_l):
		if (nnOutputValue_l is None):
			raise ValueError('nnOutputValue_l must be a list of decimal NN outputs non None')
		return np.array([x[0] for x in nnOutputValue_l])

	def __init__(self, outputValue):
		self._value = NNOutput.getNNValues(outputValue)
