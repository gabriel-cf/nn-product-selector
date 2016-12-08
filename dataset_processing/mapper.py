import json
from utils import eprint # Print to STDERR

class Mapper(object):
	""" Static class contaning methods for mapping nationality
		and category values
	"""
	# Constants
	NATIONALITY_MAPPER_FILE = "nationality_mapper.json"
	CATEGORY_MAPPER_FILE = "category_mapper.json"
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
		def readFile(fileName):
			""" Returns a file's content """
			file = open(fileName, 'rb')
			text = file.read()
			file.close()
			return text

		fileContent = readFile(fileName)
		return json.loads(fileContent)

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
	def getNationalityValue(nationality):
		return Mapper.getValue(Mapper.NATIONALITY_MAPPER_ID, nationality)

	@staticmethod
	def getCategoryValue(category):
		return Mapper.getValue(Mapper.CATEGORY_MAPPER_ID, category)

	@staticmethod
	def getGenderValue(gender):
		gender = gender.capitalize()[0]
		if (gender == 'M'):
			return '0'
		elif (gender == 'F'):
			return '1'
		else:
			eprint("Provided key for gender is neither 'M' nor 'F'")
			return None
		