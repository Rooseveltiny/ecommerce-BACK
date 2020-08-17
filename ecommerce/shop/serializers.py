from rest_framework import serializers
from shop.models import Detail, DetailGroup, Product, Category
import json


class ProductsListSerializer(serializers.ModelSerializer):

    detail = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ('link', 'title', 'unit_of_measurement',
                  'price', 'balance', 'detail')


class DetailGroupSerializer(serializers.ModelSerializer):

    class Meta:

        model = DetailGroup
        fields = ('__all__')


class DetailsSerializer(serializers.ModelSerializer):

    detail_group = DetailGroupSerializer()

    class Meta:
        model = Detail
        fields = ('__all__')

class DetailsSerializerWithOutDetailGroup(serializers.ModelSerializer):

    class Meta:
        model = Detail
        fields = ('__all__')


class ProductSerializer(serializers.ModelSerializer):

    detail = DetailsSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CatalogStructureSerializer(object):

    def __init__(self):

        pass

    def _initialize_all_objects_to_work_with(self):

        self.cats_array = []
        self.all_objects = Category.objects.all()
        self.all_none_parent_objects = self.all_objects.filter(parent=None)

    def _initialize_dict_from_object(self, source_obj):

        all_kids_array = []
        all_kids = source_obj.get_all_children()
        if len(all_kids):
            for kid in all_kids:
                all_kids_array.append(self._initialize_dict_from_object(kid))

        try:
            parent = str(source_obj.parent)
        except:
            parent = None

        obj = {
            'title': source_obj.title,
            'link': str(source_obj.link),
            'parent': parent,
            'children': all_kids_array,
            'slug': source_obj.slug
        }

        return obj

    def serialize_catalog_structure(self):

        self._initialize_all_objects_to_work_with()
        for i in self.all_none_parent_objects:
            self.cats_array.append(self._initialize_dict_from_object(i))

    def get_serialized_json(self):

        return json.dumps(self.cats_array, ensure_ascii=False)


class CategorySerializer(serializers.ModelSerializer):

    is_endpoint = serializers.BooleanField(source='check_is_endpoint', required=False)

    class Meta:

        model = Category
        fields = '__all__'


class FilterListSerializer(serializers.Serializer):

    slug = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    parameters = DetailsSerializer(many=True)


