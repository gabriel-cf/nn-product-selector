from .nninput import NNInput
from .nnoutput import NNOutput
from ...dataset_processing.modules.src.model.mappedproduct import MappedProduct
from ...dataset_processing.modules.src.model.mappeduser import MappedUser

from numbers import Number
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNTrainingInputSet(object):
	"""docstring for NNTrainingInput"""
	def addToTrainingInput(self, mapped_user, mapped_product, expected_like):
		nn_input = NNInput.getNNInput(mapped_user, mapped_product, only_entry = True)
		nn_output = NNOutput.getNNOutput(expected_like, only_entry = True)
		self._input.append(nn_input) # Concatenate in the original input list
		self._output.append(nn_output)

	def getInput(self):
		if self._converted:
			return self._input
		return np.array(self._input)
	def getOutput(self):
		if self._converted:
			return self._output
		return np.array(self._output)


	def __init__(self, x=None, y=None, rule_dic=None):
		""" x --> numpy.array([]) holding input values
			y --> numpy.array([]) holding output values
		""" 
		self._converted = False
		if (x is None or y is None):
			x = []
			y = []
		else: # numpy array from file conversion
			self._converted = True
		self._input = x
		self._output = y
		self._rule_dic = rule_dic
