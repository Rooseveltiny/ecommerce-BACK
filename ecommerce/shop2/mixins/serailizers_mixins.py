from rest_framework import serializers

class AbstractLoadingSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('__all__')
        model = None