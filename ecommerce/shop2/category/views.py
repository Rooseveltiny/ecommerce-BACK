from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.mixins.serailizers_mixins import AbstractLoadingSerializer
from shop2.category.models import Category

AbstractLoadingSerializer.Meta.model = Category

class LoadCategoryView(AbstractLoadingView):

    models_to_use = Category