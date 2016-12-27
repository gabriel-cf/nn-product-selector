import os
import json
from numbers import Number
from keras.models import Sequential
from ..dataset_processing.modules.src.model.mappedproduct import MappedProduct
from ..dataset_processing.modules.src.model.mappeduser import MappedUser

from keras.layers import Dense
from threading import RLock
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

class NNOutput(object):
	""" An object that translates a list of decimal output values into 
		a format understandable by the NN
	"""
	MAX_VALUE = 5.0

	@staticmethod
	def getNNOutput(outputValue):
		""" outputValue --> decimal value within [0, NNOutput.MAX_VALUE]
			returns --> numpy matrix where each row is an expected output
		"""
		if (not isinstance(outputValue, Number) or outputValue is None):
			raise TypeError('outputValue must be of type Number')
		t_Y = np.array([])
		# Normalize value between [0, NNOutput.MAX_VALUE]
		if (outputValue > NNOutput.MAX_VALUE):
			outputValue = 1.0
		elif (outputValue > 1.0):
			outputValue = outputValue / 5
		t_Y.append([float(outputValue)])
		return t_Y

	@staticmethod
	def translatePredictionToDecimal(nnOutputValue):
		if (nnOutputValue is None):
			raise ValueError('nnOutputValue must have a decimal value non None')
		return nnOutputValue[0]

	def __init__(self, outputValue):
		self._value = NNOutput.getNNOutput(outputValue)

class NNTrainingInputSet(object):
	"""docstring for NNTrainingInput"""
	def addToTrainingInput(mapped_user, mapped_product, expected_like):
		nn_input = NNInput(mapped_user, mapped_product)
		nn_output = NNOutput(expected_like)
		self._input.extend(nn_input._set) # Concatenate in the original input list
		self._output.extend(nn_output._set)

	def __init__(self, x=None, y=None):
		""" x --> numpy.array([]) holding input values
			y --> numpy.array([]) holding output values
		""" 
		if (x is None or y is None):
			x = np.array([])
			y = np.array([])
		self._input = x
		self._output = y
		

class NN(object):
	""" Neural network class (Thread-safe) """
	
	## Constants ##
	SCRIPT_DIR = os.path.dirname(__file__)
	CONFIG_FILE = os.path.join(SCRIPT_DIR,'config.json')

	CONFIG_DIC = None
	with open(CONFIG_FILE) as json_file:    
		CONFIG_DIC = json.load(json_file)
	SEED = 7
	NN_INPUTS = 5 # {user_nationality_mapped, user_sex_mapped, user_age, product_category_mapped}
	NN_OUTPUTS = 1 # {like_probability}
	NN_DEFAULT_EPOCHS = 70
	NN_DEFAULT_BATCH_SIZE = 10
	NN_DEFAULT_TRAINING_FILE = os.path.join(SCRIPT_DIR, CONFIG_DIC['USER_PRODUCT_TRAINING_FILE'])
	NETWORK = None # Neural Network built upon a Keras model
	## Class random init ##
	np.random.seed(SEED)
	RLOCK = RLock()

	@staticmethod
	def getInstance(loadDataFromDefaultFile=True):
		""" Singleton method to get the only instance
		"""
		if (NN.NETWORK is None):
			NN.RLOCK.acquire()
			if (NN.NETWORK is None):
				network = NN()
				network.createModel()
				if loadDataFromDefaultFile:
					network.loadTrainingDataFromFile(NN.NN_DEFAULT_TRAINING_FILE)
					network.trainModel()
				NN.NETWORK = network
			NN.RLOCK.release()
		return NN.NETWORK

	@staticmethod
	def resetNetwork():
		""" Creates a new class instance for the network
		"""
		NN.NETWORK = None
		getInstance()

	def loadTrainingDataFromFile(self, file_path, delim = ';'):
		NN.RLOCK.acquire()
		# Load dataset
		dataset = np.loadtxt(file_path, delimiter = delim)
		# Split into input (X) and output (Y) variables
		t_input = dataset[:,0:NN.NN_INPUTS]
		t_output = dataset[:,NN.NN_INPUTS]
		self._traningInputSet = NNTrainingInputSet(t_input, t_output)
		NN.RLOCK.release()

	def createModel(self):
		NN.RLOCK.acquire()
		self._model = Sequential()
		self._model.add(Dense(100, input_dim=NN.NN_INPUTS, init='normal', activation='relu')) #Dense = Fully Connected ; uniform = 0 - 0.05
		self._model.add(Dense(80, init='normal', activation='relu'))
		self._model.add(Dense(NN.NN_OUTPUTS, init='normal', activation='sigmoid'))
		# Compile model
		self._model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) #Adam = efficient gradient descent
		NN.RLOCK.release()

	def trainModel(self, nb_epoch=NN_DEFAULT_EPOCHS, batch_size=NN_DEFAULT_BATCH_SIZE):
		NN.RLOCK.acquire()
		self._model.fit(self.getTrainingInput(), self.getTrainingOutput(), nb_epoch=nb_epoch, batch_size=batch_size)
		NN.RLOCK.release()

	def evaluate(self, nn_input, nn_output):
		""" Evaluates the network's accuracy
		"""
		NN.RLOCK.acquire()
		scores = self._model.evaluate(nn_input, nn_output)
		logger.info("%s: %.2f%%" % (self._model.metrics_names[1], scores[1]*100))
		NN.RLOCK.release()
		return scores

	def predict(self, nn_input):
		""" Predicts the like value for the given input
			ev_X --> nn input in shape numpy[[user_nationality_mapped, user_sex_mapped, user_age, product_category_mapped]]
			returns --> nn output in shape numpy[[like0],[like1],..,[liken-1]] / like = float value between [0., 1.] (where '1.' is better)
		"""
		NN.RLOCK.acquire()
		prediction = self._model.predict(nn_input)
		NN.RLOCK.release()
		return prediction

	def getTrainingInput(self):
		return self._traningInputSet._input

	def getTrainingOutput(self):
		return self._traningInputSet._output

	def __init__(self):
		self._model = None
		self._traningInputSet = NNTrainingInputSet()
