from .nninput import NNInput
from .nnoutput import NNOutput
from ...dataset_processing.src.model.mappedproduct import MappedProduct
from ...dataset_processing.src.model.mappeduser import MappedUser

from numbers import Number
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNInputSet(object):
    """"""
    def add(self, mappedUser, mappedProduct):
        nn_input = NNInput.getNNValues(mappedUser, mappedProduct, only_entry=True)
        self._input.append(nn_input) # Concatenate in the original input list
        self._mappedUsers.append(mappedUser)
        self._mappedProducts.append(mappedProduct)

    def getNNValues(self):
        if self._converted:
            return self._input
        return np.array(self._input)

    def getMappedUsers(self):
        return self._mappedUsers

    def getMappedProducts(self):
        return self._mappedProducts

    def isEmpty(self):
        return len(self._input) == 0

    def __init__(self, values=None, mappedUsers=None, mappedProducts=None):
        """ values --> numpy.array([]) holding input values
        """
        self._converted = False
        if (values is None):
            values = []
            mappedUsers = []
            mappedProducts = []
        else: # numpy array from file conversion
            self._converted = True
        self._input = values
        self._mappedUsers = mappedUsers
        self._mappedProducts = mappedProducts
