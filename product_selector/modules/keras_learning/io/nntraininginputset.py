from .nninputset import NNInputSet
from .nnoutputset import NNOutputSet
from ...dataset_processing.src.model.mappedproduct import MappedProduct
from ...dataset_processing.src.model.mappeduser import MappedUser

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNTrainingInputSet(object):
    """docstring for NNTrainingInput"""
    def addRatingToTrainingInput(self, rating, valueOnly=False):
        mappedUser = rating.getMappedUser()
        mappedProduct = rating.getMappedProduct()
        ratingValue = rating.getRating()
        self._nninputset.add(mappedUser, mappedProduct, valueOnly=valueOnly)
        self._nnoutputset.add(ratingValue)

    def getInput(self):
        return self._nninputset.getNNValues()
    def getOutput(self):
        return self._nnoutputset.getNNValues()

    def __init__(self, x=None, y=None, rule_dic=None):
        """ x --> numpy.array([]) holding input values
            y --> numpy.array([]) holding output values
        """
        self._nninputset = NNInputSet(values=x)
        self._nnoutputset = NNOutputSet(values=y)
        self._rule_dic = rule_dic
