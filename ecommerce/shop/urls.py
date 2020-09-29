from django.contrib import admin
from django.urls import path, include
from shop.views import *

app_name='shop'

urlpatterns = [
    path('products/all', ProductsAllListView.as_view()),
    path('products/category/<slug:category>', ProductsCategoryListView.as_view()),
    path('products/filter/<slug:category>', FilterCategoryListView.as_view()),
    path('product/<uuid:pk>', ProductView.as_view()),
    path('catalog/categories', CategoriesView.as_view()),
    path(('catalog_structure'), CatalogStructure.as_view()),
    path(('feedback_form'), FeedBackView.as_view()),
    path(('search_products'), SearchProductsView.as_view()),
    path(('cart_list/<str:cart_uuid>'), CartListView.as_view()),
    path(('cart_product'), CartView.as_view()),

    # 1CIntegration
    path(('categories_update'), CategoriesUpdateView.as_view()),
    path(('detail_groups_update'), DetailGroupsUpdate.as_view()),
    path(('details_update'), DetailsUpdateView.as_view()),
    path(('products_update'), ProductsUpdateView.as_view()),
    path(('files_link_update'), ModelFilesUpdateView.as_view()),
]

