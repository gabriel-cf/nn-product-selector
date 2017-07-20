import logging
from ...dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ...dataset_processing.src.mapper.dbmapper import DBMapper
from ..io.nntraininginputset import NNTrainingInputSet
from ..nn import NN
from ...settings_loader import SettingsLoader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def getRules():
    dbRules = MongoHandler.getInstance().getAllRules()
    rules = DBMapper.fromDBResultToRuleDictionary(dbRules)
    return rules

class CatalogTrainer(object):
    """"""
    @staticmethod
    def trainNN(updateRules=False):
        maxDays = SettingsLoader.getValue('MAX_DAYS_RATING')
        ratingCursor = MongoHandler.getInstance().getAllRatings(maxDays=maxDays)
        trainingInputSet = NNTrainingInputSet()
        rules = None
        if updateRules:
            rules = getRules()
        i = 0
        for dbRating in ratingCursor:
            rating = DBMapper.fromDBResultToRating(dbRating)
            if rating:
                trainingInputSet.addRatingToTrainingInput(rating, valueOnly=True)
                if i % 1000 == 0:
                    logger.info("Processed %d ratings" % i)
                i += 1
        logger.info("%d ratings will be used as training data" % i)
        NN.trainNewInstance(trainingInputSet=trainingInputSet, rules=rules)
