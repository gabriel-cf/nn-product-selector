from datetime import date, datetime
from purchase import Purchase

class User(object):
	""" User object for storing data retrieved from the DB """
	def getAgeFromBirthDate(self, birthDate):
		""" Gets elapsed years from birth date"""
		today = date.today()
		years_difference = today.year - birthDate.year
		is_before_birthday = (today.month, today.day) < (birthDate.month, birthDate.day)
		elapsed_years = years_difference - int(is_before_birthday)
		return elapsed_years

	def getAgeGroup(self):
		""" Classifies person's age into one of these groups """
		if (self._age < 21):
			return 0
		elif (self._age < 35):
			return 1
		elif (self._age < 50):
			return 2
		elif (self._age < 75):
			return 3
		else:
			return 4

	def addPurchase(self, purchase):
		if (type(purchase) is Purchase):
			self._purchases.append(purchase)
		else:
			raise ValueError('purchase object must be of type Purchase')
		

	def __init__(self, username, gender, birthDay, nationality, purchases = []):
		""" username : String
			gender : M | F
			birthDay : Date
			nationality : String 
			purchases : Purchase[]
		"""
		self._username = username
		self._gender = gender
		self._age = self.getAgeFromBirthDate(birthDay)
		self._nationality = nationality
		self._ageGroup = self.getAgeGroup()
		self._purchases = purchases

