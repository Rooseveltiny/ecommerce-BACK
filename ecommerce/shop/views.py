from shop import serializers
from shop.pagination import CatalogProductsPagination
from shop.models import Product, Category, Detail, DetailGroup
from shop.views_mixins import ViewUpdateMassMixin

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
        products_queryset = Product.objects.filter(
            category__category_slug=category)

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

        # set category
        category = self.kwargs['category']

        # set sort_field
        params = dict(self.request.query_params)
        if 'sort_field' in params:
            sorting = params['sort_field'][0]
            del params['sort_field']
        else:
            sorting = 'link'

        if 'page' in params:
            del params['page']

        # select filter queryset by category
        queryset = Product.objects.filter(category__category_slug=category)

        # filter by each group params
        for group in params.keys():
            groups_params = []
            for param in params[group]:
                groups_params.append(param)
            queryset = queryset.filter(
                detail__slug__in=groups_params).distinct()

        return queryset.order_by(sorting)


class ProductView(generics.RetrieveAPIView):

    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


class CatalogStructure(View):

    def get(self, request):

        serializer = serializers.CatalogStructureSerializer()
        serializer.serialize_catalog_structure()
        json_data = serializer.get_serialized_json()

        return HttpResponse(json_data, content_type="application/json")


class CategoriesView(generics.ListAPIView):

    serializer_class = serializers.CategorySerializer

    def get_queryset(self):

        params = self.request.query_params
        if not 'parent' in params:
            return Category.get_all_parentless()
        else:
            return Category.get_all_kids_by_parants_slug(params['parent'])


class CategoriesUpdateView(ViewUpdateMassMixin):

    model_to_use = Category
    serializer_to_use = serializers.CategorySerializer
    model_name = 'Категории'

class DetailGroupsUpdate(ViewUpdateMassMixin):

    model_to_use = DetailGroup
    serializer_to_use = serializers.DetailGroupSerializer
    model_name = 'Группы характеристик'

class DetailsUpdateView(ViewUpdateMassMixin):

    model_to_use = Detail
    serializer_to_use = serializers.DetailsSerializerWithOutDetailGroup
    model_name = 'Характеристики'
