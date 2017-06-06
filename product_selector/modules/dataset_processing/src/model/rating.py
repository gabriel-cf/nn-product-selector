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

    def __lt__(self, other):
         return self._ratingValue < other._ratingValue

    def __eq__(self, other):
        return self._ratingValue == other._ratingValue

    def __repr__(self):
	    return "category:%s ; rating:%f" % (self._mProduct._mainCategory, self._ratingValue)
