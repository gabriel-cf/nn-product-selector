import json
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RecommendationEncoder(json.JSONEncoder):
	def default(self, obj):
		return obj.__dict__

class RecommendationResponse(object):
	@staticmethod
	def getJSON(recommendation):
		"""	Returns the recommendation serialized as a JSON
			and ready to be sent to the client
		"""
		json_s = json.dumps(recommendation, cls=RecommendationEncoder)
		return json.loads(json_s)
