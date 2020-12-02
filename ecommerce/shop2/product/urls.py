from django.urls import path
from shop2.product.views import LoadProductsView

urlpatterns = [
    path('load_products', LoadProductsView.as_view())
]