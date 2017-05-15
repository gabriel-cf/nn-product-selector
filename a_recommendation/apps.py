from django.apps import AppConfig
from .loader import Loader
class MyAppConfig(AppConfig):
    name = 'a_recommendation'
    verbose_name = "Recommendation Service"
    def ready(self):
    	Loader.loadNN()
    	#Loader.loadUsers()
    	Loader.loadProducts(analytics=False)
        #Loader.loadRatings()
        #Loader.loadSales()
