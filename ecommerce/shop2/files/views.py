from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.files.models import ModelFiles


class LoadFilesView(AbstractLoadingView):
    models_to_use = ModelFiles


    def post(self, request, *args, **kwargs):

        ModelFiles.objects.all().delete()
        return super().post(request, *args, **kwargs)