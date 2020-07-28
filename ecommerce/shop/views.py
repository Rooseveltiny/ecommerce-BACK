from shop import serializers 
from shop.pagination import CatalogProductsPagination
from shop.models import Product, Category

from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from ecommerce import settings
import json

# Create your views here.


class ProductsAllListView(generics.ListAPIView):

    serializer_class = serializers.ProductsListSerializer

    def get_queryset(self):

        queryset = Product.objects.all()
        return queryset


class FilterCategoryListView(generics.ListAPIView):

    serializer_class = serializers.FilterListSerializer

    def get_queryset(self):

        category = self.kwargs['category']
        products_queryset = Product.objects.filter(category__slug=category)

        # collect all details and groups
        touple_of_details = set()
        touple_of_groups = set()
        for product in products_queryset:
            for detail in product.detail.all():
                touple_of_details.add(detail)
                touple_of_groups.add(detail.detail_group)

        data = []
        for group in touple_of_groups:

            # collect all parameters
            parameters = set()
            for detail in touple_of_details:
                if detail.detail_group == group:
                    parameters.add(detail)

            # get data
            data.append(
                {
                    'name': group.title,
                    'slug': group.slug,
                    'parameters': parameters
                }
            )

        return data


class ProductsCategoryListView(generics.ListAPIView):

    serializer_class = serializers.ProductsListSerializer
    pagination_class = CatalogProductsPagination

    def get_queryset(self):

        category = self.kwargs['category']
        return Product.objects.filter(category__slug=category)


class ProductView(generics.RetrieveAPIView):

    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


class CatalogStructure(View):

    def get(self, request):

        serializer = serializers.CatalogStructureSerializer()
        serializer.serialize_catalog_structure()
        json_data = serializer.get_serialized_json()

        return HttpResponse(json_data, content_type="application/json")


class CategoriesUpdateView(APIView):

    def post(self, request, *args, **kwargs):

        queryset = Category.objects.all()
        queryset.delete()
        serializer = serializers.CategorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("all categories have been created!")
