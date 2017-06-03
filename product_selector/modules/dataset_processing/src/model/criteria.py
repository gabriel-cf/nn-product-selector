class Criteria(object):
	""" Contains parameters that
	 	define the creation of a Scenario
	"""
	def __init__(self, nationality, ageGroup, sex):
		self._nationality = nationality
		self._ageGroup = ageGroup
		self._sex = sex
