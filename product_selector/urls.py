
from django.conf.urls import url
from . import views
### This import executes the loader code when Django server starts
from .loader import Loader

urlpatterns = [
    url(r'^recommend$', views.a_recommendation, name='recommend'),
]
