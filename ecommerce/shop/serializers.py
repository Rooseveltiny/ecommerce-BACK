from rest_framework import serializers
from shop.models import Detail, DetailGroup, Product

class ProductsListSerializer(serializers.ModelSerializer):

    detail = serializers.StringRelatedField(many=True)

    class Meta: 
        model = Product
        fields = ('link', 'title', 'unit_of_measurement', 'price', 'balance', 'detail')