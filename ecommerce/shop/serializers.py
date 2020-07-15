from rest_framework import serializers
from shop.models import Detail, DetailGroup, Product

class ProductsListSerializer(serializers.ModelSerializer):

    detail = serializers.StringRelatedField(many=True)
    class Meta: 
        model = Product
        fields = ('link', 'title', 'unit_of_measurement', 'price', 'balance', 'detail')

class DetailsSerializer(serializers.ModelSerializer):

    detail_group = serializers.StringRelatedField()

    class Meta:
        model = Detail
        fields = ('title', 'link', 'detail_group')

class ProductSerializer(serializers.ModelSerializer):

    detail = DetailsSerializer(many=True)    
    class Meta:
        model = Product
        fields = '__all__'