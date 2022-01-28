from django.urls import path
from .views import index

urlpatterns = [
    path('', index),     # config/urls.py에서 'pybo/' + '' --> 'pybo/'
]