from __future__ import division
from ..enum.sexenum import Sex

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Rule(object):
	"""A rule containing the weights for the scenario generation ecuation"""

	# Constants definitions
	MAX_AGE = 90
	MAX_RATING = 5.0
	MAX_NORMALIZED_VALUE = 1.0

	def normalizeAge(self, age):
		value = 0.0
		if (age > Rule.MAX_AGE):
			value = Rule.MAX_NORMALIZED_VALUE
		else:
			value = age / Rule.MAX_AGE
		if not self._older_better:
			value = Rule.MAX_NORMALIZED_VALUE - value
		return value

	def normalizeAvgRating(self, avg_rating):
		if (avg_rating > Rule.MAX_RATING):
			return Rule.MAX_NORMALIZED_VALUE
		else:
			return avg_rating / Rule.MAX_RATING

	def getEstimatedLikeValue(self, age, sex, avg_rating):
		w_sex = self._w_male if sex == Sex.MALE else self._w_female
		# 0.0 <= Sum of weights <= Rule.MAX_RATING ; 0.0 <= normalized values <= Rule.MAX_NORMALIZED_VALUE
		like = self._w_age * self.normalizeAge(age) + w_sex + self._w_avg_rating * self.normalizeAvgRating(avg_rating)
		return like

	def __repr__(self):
		return "w_age=%.6f, w_male=%.6f, w_female=%.6f, w_avg_rating=%.6f, older_better=%r" % (self._w_age, self._w_male, self._w_female, self._w_avg_rating, self._older_better)

	def __init__(self, w_age, w_male, w_female, w_avg_rating, older_better):
		""" Intialize Rule object
			w_age --> (float) user age weight
			w_male --> (float) user male sex weight
			w_female --> (float) user female sex weight
			w_avg_rating --> (float) user average rating weight
			older_better --> (boolean) True = Yes / False = No
		"""
		self._w_age = w_age
		self._w_male = w_male
		self._w_female = w_female
		self._w_avg_rating = w_avg_rating
		self._older_better = older_better
		
