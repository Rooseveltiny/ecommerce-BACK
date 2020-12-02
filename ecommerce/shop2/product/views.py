from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.product.models import Product

class LoadProductsView(AbstractLoadingView):

    models_to_use = Product
