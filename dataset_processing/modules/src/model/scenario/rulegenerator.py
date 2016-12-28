from rule import Rule
import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RuleGenerator(object):
	""" A rule generator which randomly assigns weights to the Scenario ecuation
		and creates Rule objects. Each weight can be understood as the relevance
		that this parameter has for the final recomendation
	"""
	NUMBER_OF_PARAMETERS = 3 # user_age, user_sex, product_avg_rating
	MAX_NORMALIZED_RATING = 1.0

	@staticmethod
	def generateRule():
		""" Returns a new Rule object with all its weights randomly initialized following a Dirichlet
			distribution and the MAX_NORMALIZED_RATING that a product can have
		"""
		# Initialize random weights using Dirichlet distribution so they together sum up 1.0
		random_weights = np.random.dirichlet(np.ones(RuleGenerator.NUMBER_OF_PARAMETERS), size=1)[0]
		w_age, w_sex, w_avg_rating = random_weights #unpack weights
		# Normalize values so each weight is hold in the interval [0.0, MAX_NORMALIZED_RATING]
		w_age = w_age * RuleGenerator.MAX_NORMALIZED_RATING
		w_sex = w_sex * RuleGenerator.MAX_NORMALIZED_RATING
		w_avg_rating = w_avg_rating * RuleGenerator.MAX_NORMALIZED_RATING
		# Subdivide sex weight into female and male weights
		random_f_m_weights = np.random.dirichlet(np.ones(2), size=1)[0]
		w_male, w_female = random_f_m_weights
		w_male = w_male * w_sex
		w_female = w_female * w_sex
		# Define whether being older is better or not for the normalizeAge() method of the Rule object
		older_better = np.random.randint(0,2) == 0
		logger.debug("Generating rule with weights: w_age={}, w_male={}, w_female={}, w_avg_rating={}, older_better={}"
			.format(w_age, w_male, w_female, w_avg_rating, older_better))
		rule = Rule(w_age, w_male, w_female, w_avg_rating, older_better)

		return rule

		