from rest_framework import serializers
from shop2.detail.models import Detail, DetailGroup

class DetailGroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('link', 'slug',)
        model = DetailGroup

class DetailSerializer(serializers.ModelSerializer):

    detail_group = DetailGroupSerializer(read_only=True)

    class Meta:
        fields = ('link', 'title', 'slug', 'detail_group',)
        model = Detail