from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.mixins.serailizers_mixins import AbstractLoadingSerializer
from shop2.category.models import Category
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
import json

AbstractLoadingSerializer.Meta.model = Category

class LoadCategoryView(AbstractLoadingView):

    models_to_use = Category

class CatalogStructureView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):

        json_data = json.dumps(Category.get_catalog_structure(), ensure_ascii=False)
        return HttpResponse(json_data, content_type="application/json")  
