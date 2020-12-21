from django.urls import path
from shop2.product.views import LoadProductsView, ProductsListView, ProductCardView

urlpatterns = [
    path('load_products', LoadProductsView.as_view()),
    path('products/category/<str:category>', ProductsListView.as_view()),
    path('product/<uuid:pk>', ProductCardView.as_view()),
]