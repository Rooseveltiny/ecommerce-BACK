from rest_framework import serializers
from shop2.category.models import Category

class CategorySerailzer(serializers.ModelSerializer):

    class Meta:

        fields = ('__all__')
        models = Category

        