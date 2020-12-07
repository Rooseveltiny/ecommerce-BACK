from django.urls import path
from shop2.category.views import LoadCategoryView, CatalogStructureView

urlpatterns = [
    path('load_categories', LoadCategoryView.as_view()),
    path('catalog_structure', CatalogStructureView.as_view()),
]