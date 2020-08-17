from rest_framework.views import APIView
from rest_framework.response import Response


'''
Mixin for massiv uploading data
'''


class ViewUpdateMassMixin(APIView):

    model_to_use = None
    serializer_to_use = None
    model_name = ''
    success_message = 'успешно выгружены!'

    def post(self, request, *args, **kwargs):

        queryset = self.model_to_use.objects.all()
        queryset.delete()
        serializer = self.serializer_to_use(
            data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("{} {}".format(self.model_name, self.success_message))
