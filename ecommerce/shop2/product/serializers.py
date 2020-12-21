from rest_framework import serializers
from shop2.product.models import Product
from shop2.detail.serializers import DetailForProductsListSerializer


class ProductReadSerializer(serializers.ModelSerializer):

    files = serializers.DictField(source='all_objects_files')
    details = DetailForProductsListSerializer(many=True)
    price = serializers.StringRelatedField(source='get_price', read_only=True)
    balance = serializers.StringRelatedField(
        source="get_balance", read_only=True)

    class Meta:
        model = Product
        fields = ('__all__')


class ProductListReadSerializer(ProductReadSerializer):

    files = serializers.DictField(source='all_objects_files')
    details = DetailForProductsListSerializer(many=True)
    price = serializers.StringRelatedField(source='get_price', read_only=True)
    balance = serializers.StringRelatedField(
        source="get_balance", read_only=True)

    class Meta:
        model = Product
        fields = ('__all__')
