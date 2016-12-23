import json
from keras.models import Sequential
from keras.layers import Dense
from threading import RLock
import numpy
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NN(object):
	""" Neural network class (Thread-safe) """
	
	## Constants ##
	CONFIG_FILE = 'config.json'
	CONFIG_DIC = None
	with open(CONFIG_FILE) as json_file:    
		CONFIG_DIC = json.load(json_file)
	SEED = 7
	NN_INPUTS = 3 # {user_nationality_mapped, user_sex_mapped, user_age, product_category_mapped}
	NN_OUTPUTS = 1 # {like_probability}
	NN_DEFAULT_EPOCHS = 150
	NN_DEFAULT_BATCH_SIZE = 10
	NN_DEFAULT_TRAINING_FILE = CONFIG_DIC['DEFAULT_TRAINING_FILE']
	NETWORK = None # Neural Network built upon a Keras model
	## Class random init ##
	numpy.random.seed(SEED)
	RLOCK = RLock()

	@staticmethod
	def getInstance():
		""" Singleton method to get the only instance
		"""
		if (NN.NETWORK is None):
			NN.RLOCK.acquire()
			if (NN.NETWORK is None):
				network = NN()
				network.createModel()
				network.loadTrainingDataFromFile(NN.NN_DEFAULT_TRAINING_FILE)
				network.trainModel()
				NN.NETWORK = network
			NN.RLOCK.release()
		return NN.NETWORK

	def loadTrainingDataFromFile(self, file_path, delim = ';'):
		NN.RLOCK.acquire()
		# Load dataset
		dataset = numpy.loadtxt(file_path, delimiter = delim)
		# Split into input (X) and output (Y) variables
		self._t_X = dataset[:,0:3]
		self._t_Y = dataset[:,3]
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
		self._model.fit(self._t_X, self._t_Y, nb_epoch=nb_epoch, batch_size=batch_size)
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

	def __init__(self):
		self._model = None
		self._t_X = None
		self._t_Y = None
