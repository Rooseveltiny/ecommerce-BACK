from django.urls import path
from shop2.filter_catalog.views import FilterCatalogView

urlpatterns = [
    path('catalog_filter/<str:category>', FilterCatalogView.as_view()),
]