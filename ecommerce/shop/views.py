from shop.serializers import ProductsListSerializer, ProductSerializer, SerializeCatalogStructure, CategorySerializer
from shop.models import Product, Category
from ecommerce import settings

from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import json

# Create your views here.


class ProductsAllListView(generics.ListAPIView):

    serializer_class = ProductsListSerializer
    queryset = Product.objects.all()


class ProductsCategoryListView(generics.ListAPIView):

    serializer_class = ProductsListSerializer

    def get_queryset(self):

        category = self.kwargs['category']
        return Product.objects.filter(category__slug=category)


class ProductView(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CatalogStructure(View):

    def get(self, request):

        serializer = SerializeCatalogStructure()
        serializer.serialize_catalog_structure()
        json_data = serializer.get_serialized_json()

        return HttpResponse(json_data, content_type="application/json")


class CategoriesUpdateView(APIView):


    def post(self, request, *args, **kwargs):

        queryset = Category.objects.all()
        queryset.delete()
        serializer = CategorySerializer(data = request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("all categories have been created!")