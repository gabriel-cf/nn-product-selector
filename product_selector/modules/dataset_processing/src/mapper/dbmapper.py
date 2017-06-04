import logging
from datetime import datetime
from ..io.mongoconnector.mongohandler import MongoHandler
from ..model.user import User
from ..model.product import Product
from ..model.mappeduser import MappedUser
from ..model.mappedproduct import MappedProduct
from ..model.rating import Rating

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBMapper(object):
    """Static class that maps a user from the MongoDB into a processable user"""

    @staticmethod
    def fromDBResultToUser(dbUser):
        """ Receives the dictionary result of the query against
            the DB and returns an array of mapped User objects
        """
        username = dbUser['login']['username']
        gender = dbUser['gender']
        dateOfBirth = dbUser['dob'] #yyyy-mm-dd
        nationality = dbUser['nat']
        # Transform string date to date object
        dateOfBirth = datetime.strptime(dateOfBirth.split(' ')[0], '%Y-%m-%d')
        logger.debug("Mapped user: %s;%s;%d;%s", username, gender, dateOfBirth.year, nationality)
        user = User(username, gender, dateOfBirth, nationality)

        return user

    @staticmethod
    def fromDBResultToMappedUser(dbUser):
        user = DBMapper.fromDBResultToUser(dbUser)
        if user:
            return MappedUser(user)
        return None

    @staticmethod
    def fromDBResultToProduct(dbProduct):
        """ Receives the dictionary result of the query against
            the DB and returns an array of mapped Product objects.
            Will return None if the product cannot be correctly mapped.
        """
        product = None
        idP = dbProduct['_id']
        name = dbProduct['name']
        categories = dbProduct['sections']
        imageUrl = dbProduct['image_url']
        if (categories):
            product = Product(idP, name, categories, imageUrl)
            logger.debug("Mapped product: prod_id:%s", idP)

        return product

    @staticmethod
    def fromDBResultToMappedProduct(dbProduct):
        product = DBMapper.fromDBResultToProduct(dbProduct)
        if product:
            return MappedProduct(product)
        return None

    @staticmethod
    def fromDBResultToRating(dbRating):
        """This method will actually call the MongoHandler again in order to
           retrieve the user and the product associated with the id
        """
        rating = None
        ratingValue = dbRating['_rating']
        productId = dbRating['_productId']
        username = dbRating['_userId']
        dbUser = MongoHandler.getInstance().getUsersByParameters(one_only=True, username=username)
        dbProduct = MongoHandler.getInstance().getProductsByParameters(one_only=True, id=productId)
        user = DBMapper.fromDBResultToMappedUser(dbUser)
        product = DBMapper.fromDBResultToMappedProduct(dbProduct)
        if (not user is None and not product is None):
            rating = Rating(ratingValue, user, product)
            logger.debug("Mapped rating: ratingValue:%d, username:%s, productId:%s",\
                         ratingValue, username, productId)

        return rating
