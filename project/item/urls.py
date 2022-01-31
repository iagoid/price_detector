from django.urls import path
from . import views

urlpatterns = [
    path('', views.itemsList, name='item-list'),
    path('delete/<int:id>', views.deleteItem, name="delete-task"),
]
