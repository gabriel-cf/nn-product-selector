import logging
from ...dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ...dataset_processing.src.mapper.dbmapper import DBMapper
from ...recommender_engine.db_to_nn_input_processor import DBToNNInputProcesor
from ..io.nntraininginputset import NNTrainingInputSet
from ..nn import NN

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
        ratingCursor = MongoHandler.getInstance().getAllRatings()
        trainingInputSet = NNTrainingInputSet()
        rules = None
        if updateRules:
            rules = getRules()
        i = 0
        ratingTest = None
        for dbRating in ratingCursor:
            rating = DBMapper.fromDBResultToRating(dbRating)
            if rating:
                trainingInputSet.addRatingToTrainingInput(rating)
                i += 1
                if i %500 == 0:
                    ratingTest = rating
                    break
                if i % 1000 == 0:
                    logger.info("Processed %d ratings" % i)
        logger.info("%d ratings will be used as training data" % i)
        NN.trainNewInstance(trainingInputSet=trainingInputSet, rules=rules)
        #prediction = NN.getInstance().predict(trainingInputSet.getInput())
        #realRating = trainingInputSet.getOutput()
        #print(prediction - realRating)
