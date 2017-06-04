class Rating(object):
    """"""
    def __init__(self, mUser, mProduct, ratingValue):
        self._mUser = mUser
        self._mProduct = mProduct
        self._ratingValue = ratingValue

    def getRating(self):
        return self._ratingValue

    def getMappedUser(self):
        return self._mUser

    def getMappedProduct(self):
        return self._mProduct
