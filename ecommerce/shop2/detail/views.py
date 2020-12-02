from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.mixins.serailizers_mixins import AbstractLoadingSerializer
from shop2.detail.models import DetailGroup, Detail


class LoadDetailView(AbstractLoadingView):

    models_to_use = Detail
    

class LoadDetailGroupsView(AbstractLoadingView):

    models_to_use = DetailGroup