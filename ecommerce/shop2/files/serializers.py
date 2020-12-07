from rest_framework import serializers
from shop2.files.models import ModelFiles


class ObjectsFilesSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('__all__',)
        model = ModelFiles