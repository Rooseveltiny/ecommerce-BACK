from rest_framework import serializers
from shop2.detail.models import Detail, DetailGroup


class DetailGroupReadSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title',)
        model = DetailGroup


class DetailForProductsListSerializer(serializers.ModelSerializer):

    group = serializers.StringRelatedField(source="get_detail_group_title")

    class Meta:
        fields = ('group', 'title')
        model = Detail