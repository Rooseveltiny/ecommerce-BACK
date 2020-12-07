from django.urls import path
from shop2.balance.views import LoadBalancesView

urlpatterns = [
    path('load_balance', LoadBalancesView.as_view()),
]