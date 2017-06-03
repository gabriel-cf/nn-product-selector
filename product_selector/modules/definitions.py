import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def getDictionary(fileName):
	""" Returns a JSON which can be accessed
	 	as a dictionary
	"""
	with open(fileName) as data_file:    
		data = json.load(data_file)

	return data
def loadPath(fileName, config_dic):
	""" Returns the path specified in the configuration dictionary
		if and only if it is a valid path
	"""
	path = os.path.join(ROOT_DIR, config_dic[fileName])
	if (not os.path.exists(path)):
		raise ValueError("For file '%s' the retrieved path '%s' was not valid" % (fileName, path))
	return path

CONFIG_FILE = os.path.join(ROOT_DIR,'config.json')
CONFIG_DIC = getDictionary(CONFIG_FILE)

# KEY NAMES DECLARATIONS
NN_TRAINING_FILE_NAME = 'USER_PRODUCT_TRAINING_FILE'
MAPPER_NATIONALITY_FILE_NAME = 'NATIONALITY_MAPPER_FILE'
MAPPER_CATEGORY_FILE_NAME = 'CATEGORY_MAPPER_FILE'
# Absolute path retrieval
NN_TRAINING_FILE = loadPath(NN_TRAINING_FILE_NAME, CONFIG_DIC)
MAPPER_NATIONALITY_FILE = loadPath(MAPPER_NATIONALITY_FILE_NAME, CONFIG_DIC)
MAPPER_CATEGORY_FILE = loadPath(MAPPER_CATEGORY_FILE_NAME, CONFIG_DIC)


