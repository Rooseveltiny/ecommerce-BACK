from rest_framework.views import APIView
from shop2.product.models import Product
from rest_framework.response import Response
from shop2.filter_catalog.serializers import DetailSerializer
import json

class FilterCatalogView(APIView):

    def get(self, request, *args, **kwargs):

        category = self.kwargs['category']
        products_queryset = Product.objects.filter(
            products_category__slug=category)

        # collect all details and groups
        touple_of_details = set()
        touple_of_groups = set()
        for product in products_queryset:
            for detail in product.details.all():
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

            data.append(
                {
                    'name': group.title,
                    'slug': group.slug,
                    'input_type': 'checkbox',
                    'parameters': DetailSerializer(parameters, many=True).data,
                }
            )

        return Response(data, content_type="application/json") 
