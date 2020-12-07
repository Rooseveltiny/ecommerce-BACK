from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.price.models import Price

class LoadPricesView(AbstractLoadingView):
    look_fields = ('product', 'title',)
    models_to_use = Price