from shop import serializers
from shop.pagination import CatalogProductsPagination
from shop.models import Product, Category, Detail, DetailGroup, ModelFiles, FeedBack, Cart, FAQ
from shop.views_mixins import ViewUpdateMassMixin

from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.views import View

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ecommerce import settings
from shop.additional_modules import CheckGrammar
import json
from uuid import uuid4

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
            category__slug=category)

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

            # check whether there's the only one parameter
            if len(parameters) < 2:
                continue
            parameters = sorted(parameters, key=lambda k: k.title) 
            
            # get data
            data.append(
                {
                    'name': group.title,
                    'slug': group.slug,
                    'parameters': parameters,
                    'input_type': 'checkbox',
                }
            )

        # here we can add price

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
        queryset = Product.objects.filter(category__slug=category)

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


class ModelFilesUpdateView(ViewUpdateMassMixin):

    model_to_use = ModelFiles
    serializer_to_use = serializers.ModelFilesSerializer
    model_name = 'Ссылки на файлы объектов'


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
    serializer_to_use = serializers.DetailsSerializerForUpdate
    model_name = 'Характеристики'


class ProductsUpdateView(ViewUpdateMassMixin):

    model_to_use = Product
    serializer_to_use = serializers.ProductsListSerializerForUpdate
    model_name = 'Номенклатуры'


class FeedBackView(generics.CreateAPIView):

    serializer_class = serializers.FeedBackSerializer


class SearchProductsView(APIView):

    def make_query(self, input_value):

        products = Product.objects.filter(title__contains=input_value)
        categories = Category.objects.filter(title__contains=input_value)
        nothing_found = not len(products) and not len(categories) 

        search_result = {
            'products': products,
            'categories': categories,
            'nothing_found': nothing_found,
        }

        return search_result

    def get_queryset(self):

        input_value = self.request.query_params['search_input_value']
        search_data = self.make_query(input_value)

        if search_data['nothing_found']:
            input_value = CheckGrammar(input_value).corrected_text
            if len(input_value):
                search_data = self.make_query(input_value)

        return search_data

    def get(self, request):

        data = serializers.SearchResultSerializer(self.get_queryset()).data
        return HttpResponse(json.dumps(data), content_type="application/json")


class CartListView(generics.ListAPIView):

    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(cart_uuid=self.kwargs['cart_uuid'])


class CartView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):

    serializer_class = serializers.CartSerializer
    product_in_cart = None

    def _init_attributes(func):
        def wrapper_set_attributes(self, request, *args, **kwargs):
            self.data = request.data.copy()
            self._set_product_in_cart_instance()
            return func(self, request, *args, **kwargs)
        return wrapper_set_attributes

    def _set_product_in_cart_instance(self):
        self.product_in_cart = Cart.objects.filter(product=self.data['product'], cart_uuid=self.data['cart_uuid']).first()

    def add_to_cart(self):

        if self.product_in_cart:
            plus_value = self.data['quantity'] if self.data['quantity'] > 0 else self.data['quantity'] * -1
            self.data['quantity'] = self.product_in_cart.quantity + plus_value
            return self.validate_and_update()
        else:
            return self.validate_and_create()

    def validate_and_update(self):

        instance = self.product_in_cart
        serializer = self.get_serializer(instance, data=self.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def validate_and_create(self):

        serializer = self.get_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self):
        if self.product_in_cart:
            self.perform_destroy(self.product_in_cart)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @_init_attributes
    def post(self, request, *args, **kwargs):

        if  request.user.is_authenticated:
            pass
        elif self.data['cart_uuid']:
            return self.add_to_cart()
        else:
            cart_uuid = uuid4()
            self.data['cart_uuid'] = cart_uuid
            response_object = self.add_to_cart()
            if response_object.status_code == 201:
                response_object.data['cart_uuid'] = cart_uuid
                return response_object
            else:
                return response_object
        
    @_init_attributes
    def delete(self, request, *args, **kwargs):

        return self.destroy()

    @_init_attributes
    def put(self, request, *args, **kwargs):

        return self.validate_and_update()


class FAQView(ViewUpdateMassMixin):

    model_to_use = FAQ
    serializer_to_use = serializers.FAQSerializer
    model_name = "вопросы и ответы"
