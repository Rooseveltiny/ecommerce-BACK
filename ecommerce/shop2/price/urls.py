from django.urls import path
from shop2.price.views import LoadPricesView

urlpatterns = [
    path('load_prices', LoadPricesView.as_view()),
]
