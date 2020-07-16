from django.contrib import admin
from django.urls import path, include
from shop.views import *

app_name='shop'

urlpatterns = [
    path('products/all', ProductsListView.as_view()),
    path('product/<uuid:pk>', ProductView.as_view()),
    path(('categories'), Categories.as_view()),
]
