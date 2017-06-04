import logging
import numpy as np
from .nnoutput import NNOutput

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NNOutputSet(object):
    """"""
    def add(self, ratingValue):
        nn_output = NNOutput.getNNOutput(ratingValue, only_entry=True)
        self._values.append(nn_output)

    def getValues(self):
        if self._converted:
            return self._values
        return np.array(self._values)

    def __init__(self, values=None):
        """ values --> numpy.array([]) holding output values
        """
        self._converted = False
        if (values is None):
            values = []
        else: # numpy array from file conversion
            self._converted = True
        self._values = values
