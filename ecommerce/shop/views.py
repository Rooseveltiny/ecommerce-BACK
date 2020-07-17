from shop.serializers import ProductsListSerializer, ProductSerializer, SerializeCatalogStructure
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from shop.models import Product, Category
from rest_framework import generics
from ecommerce import settings
from django.views import View
import json

# Create your views here.


class ProductsListView(generics.ListAPIView):

    serializer_class = ProductsListSerializer
    queryset = Product.objects.all()


class ProductView(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class Categories(View):

    def get(self, request):

        with default_storage.open("categories.json") as file:

            data = json.load(file)
            return JsonResponse(data, safe=False)


class CatalogStructure(View):

    def get(self, request):

        serializer = SerializeCatalogStructure()
        serializer.serialize_catalog_structure()
        json_data = serializer.get_serialized_json()

        return HttpResponse(json_data, content_type="application/json")
