from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.balance.models import Balance

class LoadBalancesView(AbstractLoadingView):
    look_fields = ('place', 'product',)
    models_to_use = Balance