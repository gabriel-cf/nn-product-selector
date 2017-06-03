from .product import Product

class Category(object):
    """Category object holding the list of recommended products"""

    def __init__(self, name):
        self._categoryName = name
        self._productList = []

    def add(self, product):
        self._productList.append(product)

    def isComplete(self, maxProducts):
        return len(self._productList) >= maxProducts
