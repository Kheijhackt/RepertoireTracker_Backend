from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('privacy/', privacy, name='privacy'),
    path('terms/', terms, name='terms'),
]