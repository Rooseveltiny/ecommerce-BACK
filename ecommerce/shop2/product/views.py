from shop2.mixins.views_mixins import AbstractLoadingView
from shop2.category.models import Category
from shop2.product.models import Product
from shop2.detail.models import Detail
from rest_framework.generics import ListAPIView
from shop2.product.serializers import ProductReadSerializer
from shop2.paginations import CatalogProductsPagination


class LoadProductsView(AbstractLoadingView):

    models_to_use = Product

    def create_or_update(self, instance, input_data_item):

        all_details = input_data_item.pop('details')
        link = input_data_item.pop('link')
        category = Category.objects.filter(
            link=input_data_item['products_category']).first()
        input_data_item['products_category'] = category

        product_item, created = Product.objects.update_or_create(
            link=link, defaults=input_data_item)
        if created:
            self.created_elements += 1
        else:
            self.updated_elements += 1

        for detail_link in all_details:
            detail_item = Detail.objects.filter(link=detail_link).first()
            if detail_item:
                product_item.details.add(detail_item)


class ProductsListView(ListAPIView):

    pagination_class = CatalogProductsPagination
    serializer_class = ProductReadSerializer
    queryset = Product.objects.all()

    def filter_queryset_by_category(self):

        self.queryset = self.queryset.filter(
            products_category__slug=self.kwargs['category'])

    def filter_queryset_by_params(self):

        params = dict(self.request.query_params)
        if 'page' in params:
            del params['page']
        if 'sort_field' in params:
            del params['sort_field']

        for group in params.keys():
            groups_params = []
            for param in params[group]:
                groups_params.append(param)
            self.queryset = self.queryset.filter(
                details__slug__in=groups_params).distinct()

    def sort_queryset_by_sorting_field(self):

        params = dict(self.request.query_params)
        if 'sort_field' in params:
            sorting = params['sort_field'][0]
        else:
            sorting = 'link'

        self.queryset = self.queryset.order_by(sorting)

    def get_queryset(self):

        self.filter_queryset_by_category()
        self.filter_queryset_by_params()
        self.sort_queryset_by_sorting_field()
        return self.queryset

