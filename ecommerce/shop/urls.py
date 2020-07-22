from django.contrib import admin
from django.urls import path, include
from shop.views import *

app_name='shop'

urlpatterns = [
    path('products/all', ProductsAllListView.as_view()),
    path('products/category/<slug:category>', ProductsCategoryListView.as_view()),
    path('products/filter/<slug:category>', FilterCategoryListView.as_view()),
    path('product/<uuid:pk>', ProductView.as_view()),
    path(('catalog_structure'), CatalogStructure.as_view()),
    path(('categories_update'), CategoriesUpdateView.as_view()),
]
