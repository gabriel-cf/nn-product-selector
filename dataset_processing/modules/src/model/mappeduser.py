from datetime import date, datetime
from ..mapper.mapper import Mapper
from enum.sexenum import Sex

class MappedUser(object):
	""" MappedUser object for storing data retrieved from the DB """

	def __init__(self, user):
		""" Takes a user object and returns a mapped user 
			Fields mapped match those needed by the NN
		""" 
		self._gender = Mapper.getGenderValue(user._gender)
		self._nationality = Mapper.getNationalityValue(user._nationality)
		self._age = user._age
