from .product import Product

class Category(object):
    """Category object holding the list of recommended products"""

    def __init__(self, name, productList=None):
        self._categoryName = name
        self._productList = productList
        if not self._productList:
            self._productList = []

    def getCategoryName(self):
        return self._categoryName

    def getProductList(self):
        return self._productList

    def add(self, product):
        self._productList.append(product)

    def isComplete(self, maxProducts):
        return len(self._productList) >= maxProducts
