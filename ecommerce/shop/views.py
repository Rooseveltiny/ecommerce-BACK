from shop.serializers import ProductsListSerializer, ProductSerializer
from django.http import JsonResponse
from rest_framework import generics
from django.shortcuts import render
from shop.models import Product
from django.views import View
from ecommerce import settings
from django.core.files.storage import default_storage
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
