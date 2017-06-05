from django.apps import AppConfig
from .modules.keras_learning.training.catalog_trainer import CatalogTrainer
from .loader import Loader
class MyAppConfig(AppConfig):
    name = 'a_recommendation'
    verbose_name = "Recommendation Service"
    def ready(self):
        CatalogTrainer.trainNN(updateRules=True)
    	#Loader.loadNN()
    	#Loader.loadUsers()
    	#Loader.loadProducts(analytics=False)
        #Loader.loadRatings()
        #Loader.loadSales()
