from ..settings_loader import SettingsLoader
from ..dataset_processing.src.model.category import Category

class CategorySet(object):
    """A set of categories meant to be used while passing products sorted by
       the highest rating prediction. It will return a number of categories given
       by the param {MAX_CATEGORIES} in config.json where each one
       will have a number products given by {MAX_PRODUCTS_PER_CATEGORY}.
       It simply fills the categories as the products come in, storing them in the final
       stage when they are completed, being the CategorySet itself completed when max
       categories have made it to final.
    """
    MAX_CATEGORIES = SettingsLoader.getValue("MAX_CATEGORIES")
    MAX_PRODUCTS = SettingsLoader.getValue('MAX_PRODUCTS_PER_CATEGORY')
    def __init__(self):
        self._finalCategories = []
        self._categoryDict = dict()

    def addProduct(self, product):
        """ """
        categoryName = product.getCategory()
        if not self._hasCategory(categoryName):
            self._createCategory(categoryName)
        if not self._isCategoryComplete(categoryName):
            self._addToCategory(categoryName, product)
            if self._isCategoryComplete(categoryName):
                self._addToFinalCategories(categoryName)

    def getFinalCategories(self):
        return self._finalCategories

    def isComplete(self):
        return len(self._finalCategories) >= CategorySet.MAX_CATEGORIES

    def _createCategory(self, categoryName):
        self._categoryDict[categoryName] = Category(categoryName)

    def _hasCategory(self, categoryName):
        return categoryName in self._categoryDict

    def _isCategoryComplete(self, categoryName):
        category = self._categoryDict[categoryName]
        return category.isComplete(CategorySet.MAX_PRODUCTS)

    def _addToCategory(self, categoryName, product):
        category = self._categoryDict[categoryName]
        category.add(product)

    def _addToFinalCategories(self, categoryName):
        category = self._categoryDict[categoryName]
        self._finalCategories.append(category)
