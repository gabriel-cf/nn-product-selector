
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^recommend$', views.a_recommendation, name='recommend'),
]
