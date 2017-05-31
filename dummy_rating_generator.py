"""
    This script loads into the MongoDB test rating documents
    ## MOCK COLLECTIONS WILL BE DROPPED ##
    Rules will be loaded to rules_collection_mock
    Ratings will be loaded to ratings_collection_mock
"""


import random
import time
from .a_recommendation.modules.dataset_processing.modules.src.io.mongoconnector.mongohandler import MongoHandler
from .a_recommendation.modules.dataset_processing.modules.src.model.scenario.scenariogenerator import ScenarioGenerator
from .a_recommendation.modules.dataset_processing.modules.src.mapper.mapper import Mapper
from .a_recommendation.loader import Loader

handler = MongoHandler.getInstance()
MAX_DAYS = 30

def dropCollections():
    handler._analysisDB.rules_collection_mock.drop()
    handler._analysisDB.ratings_collection_mock.drop()
    handler._analysisDB.sales_collection_mock.drop()

def insertRule(nationality, category, rule):
    doc = {
        "_nationality": nationality,
        "_category": category,
        "_w_age": rule._w_age,
        "_w_male": rule._w_male,
        "_w_female": rule._w_female,
        "_w_avg_rating": rule._w_avg_rating,
        "_older_better": rule._older_better
    }
    #print "RULES-_nationality:{};_category:{};_w_age:{};_w_male:{};_w_female:{};_w_avg_rating:{};_older_better:{}"\
    #.format(nationality, category, rule._w_age, rule._w_male, rule._w_female, rule._w_avg_rating, rule._older_better)
    handler._analysisDB.rules_collection_mock.insert_one(doc)

def insertRatingAndSale(user, product, estimated_rating):
    # Generate random number of days old possibly slightly over the max number
    # A 5% aproximately should be out of range
    days = (MAX_DAYS + MAX_DAYS * 0.05) * random.random()
    date = time.time() - (days * 24 * 3600)
    docRating = {
        '_productId': product._id,
        '_userId': user._username,
        '_date': date,
        '_productRating': product._avgRating,
        '_rating': estimated_rating
    }
    #docSale = {
    #    '_productId': product._id,
    #    '_userId': user._username,
    #    '_date': date,
    #    '_productRating': product._avgRating
    #}
    #print "RATINGS-_productId:{};_userId:{};_date:{};_rating:{}".format(product._id, user._username, date, estimated_rating)
    #print "SALES-_productId:{};_userId:{};_date:{}".format(product._id, user._username, date)
    handler._analysisDB.ratings_collection_mock.insert_one(docRating)
    #handler._analysisDB.sales_collection_mock.insert_one(docSale)

def randomTrue():
    return random.random() < 0.5

if __name__ == '__main__':
    # Drop collections, otherwise it will generate contradictions
    dropCollections()
    # Generate rules (m_nationality, m_category)
    # Each rule will give us the rating for a given combination of user with product
    # Rules are generated randomly, the weight for each user and product factor is random
    # Additionally, sometimes being older may produce better ratings:
    # e.g. rule('ES', Female, 17yo ; 'Books', '3.8') --> 3.2
    # e.g. rule('ES', Female, 66yo ; 'Books', '3.8') --> 4.9
    # Or worse:
    # e.g. rule('ES', Female, 17yo ; 'Video Games', '3.8') --> 4.2
    # e.g. rule('ES', Female, 66yo ; 'Video Games', '3.8') --> 2.0
    # This is also random
    rules_dic = ScenarioGenerator.generateTrainingInputSet()._rule_dic
    users_dic, users_m_dic = Loader.loadUsers()
    products_dic, products_m_dic = Loader.loadProducts(analytics=False)

    #Load rules into DB. These are used for reference
    nationalities = Mapper.getAllAvailableNationalities()
    categories = Mapper.getAllAvailableCategories()

    for nationality in nationalities:
        for category in categories:
            rule = rules_dic[(Mapper.getNationalityValue(nationality), Mapper.getCategoryValue(category))]
            insertRule(nationality, category, rule)

    # combine users X products
    # The number of users and products is limited by the constant dMAX in loader.py
    count = 0
    #random_weights = np.random.dirichlet(np.ones(len(users_dic.keys())), size=1)[0]
    for nationality, users in users_dic.items():
        print(nationality)
        for i in range(0, len(users)):
            if randomTrue():
                continue
            user = users[i]
            m_user = users_m_dic[nationality][i]
            for category, products in products_dic.items():
                if randomTrue():
                    continue
                for j in range(0, len(products)):
                    if randomTrue():
                        continue
                    product = products[j]
                    m_product = products_m_dic[category][j]
                    estimated_rating = rule.getEstimatedLikeValue(m_user, m_product)
                    insertRatingAndSale(user, product, estimated_rating)
                    count += 1
    print(count)
    print("Creating indexes for _productId and _userId")
    handler._analysisDB.ratings_collection_mock.create_index([('_productId', 1)])
    handler._analysisDB.ratings_collection_mock.create_index([('_userId', 1)])
