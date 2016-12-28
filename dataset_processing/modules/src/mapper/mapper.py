import os
import json
from ..util.utils import eprint # Print to STDERR
from ..model.enum.sexenum import Sex

class Mapper(object):
	""" Static class contaning methods for mapping nationality
		and category values
	"""
	# Constants
	NATIONALITY_MAPPER_FILE = "{0}/{1}".format(os.environ['DATA_PROCESSING_DIR'], 'modules/config/mapper/nationality_mapper.json')
	CATEGORY_MAPPER_FILE = "{0}/{1}".format(os.environ['DATA_PROCESSING_DIR'], 'modules/config/mapper/category_mapper.json')
	NATIONALITY_MAPPER_ID = "nationality_mapper"
	CATEGORY_MAPPER_ID = "category_mapper"

	# Static variables
	nationality_mapper = None
	category_mapper = None

	@staticmethod
	def getDictionary(fileName):
		""" Returns a JSON which can be accessed
		 	as a dictionary
		"""
		with open(fileName) as data_file:    
			data = json.load(data_file)

		return data

	@staticmethod
	def updateMappers():
		""" Updates mappers with the current contents
		 	of the mapping files
		"""
		Mapper.nationality_mapper = Mapper.getDictionary(Mapper.NATIONALITY_MAPPER_FILE)
		Mapper.category_mapper = Mapper.getDictionary(Mapper.CATEGORY_MAPPER_FILE)

	@staticmethod
	def getValue(mapper, key):
		""" Generic function for retrieving a value from a selected mapper
			mapper --> MAPPER_ID of mapper associated to key
			key --> key to map
		"""
		# Update mappers if they are not initialized yet
		if (Mapper.nationality_mapper is None or Mapper.category_mapper is None):
			Mapper.updateMappers()
		# Select appropiate mapper
		if(mapper == Mapper.NATIONALITY_MAPPER_ID):
			mapper = Mapper.nationality_mapper
		else:
			mapper = Mapper.category_mapper
		value = None
		# Try to retrieve associated value
		try:
			value = mapper[key]
		except KeyError:
			eprint("Provided Key '{0}' is not a valid key".format(key))
		return value

	@staticmethod
	def getAllAvailableNationalities():
		if (Mapper.nationality_mapper is None):
			Mapper.updateMappers()
		return Mapper.nationality_mapper.keys()

	@staticmethod
	def getAllAvailableCategories():
		if (Mapper.category_mapper is None):
			Mapper.updateMappers()
		return Mapper.category_mapper.keys()

	@staticmethod
	def getNationalityValue(nationality):
		return Mapper.getValue(Mapper.NATIONALITY_MAPPER_ID, nationality)

	@staticmethod
	def getCategoryValue(category):
		return Mapper.getValue(Mapper.CATEGORY_MAPPER_ID, category)

	@staticmethod
	def getGenderValue(gender):
		if (gender == Sex.MALE):
			return '0'
		elif (gender == Sex.FEMALE):
			return '1'
		else:
			raise ValueError("Provided key %s for gender is neither Sex.MALE nor Sex.FEMALE" % (gender))
