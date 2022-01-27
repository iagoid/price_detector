from django.urls import path
from . import views

urlpatterns = [
    path('', views.itemsList, name='item-list'),
]
