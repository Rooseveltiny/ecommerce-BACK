from rest_framework.views import APIView
from rest_framework.response import Response
from shop2.mixins.serailizers_mixins import AbstractLoadingSerializer

class AbstractLoadingView(APIView):

    look_field = 'link'
    serailizer_to_use = None
    models_to_use = None

    updated_elements = 0
    created_elements = 0
    raised_exceptions = []

    def __init__(self, *args, **kwargs):

        serailizer = AbstractLoadingSerializer
        serailizer.Meta.model = self.models_to_use
        self.serailizer_to_use = serailizer

    @property
    def get_response(self):
        return f'Created: {self.created_elements}. Updated: {self.updated_elements}. errors: {self.raised_exceptions}'

    def get_instance(self, input_data_item):

        search_kwarg = {self.look_field: input_data_item[self.look_field]}
        return self.models_to_use.objects.filter(**search_kwarg).first()

    def create_or_update(self, instance, input_data_item):

        if instance:
            serializer = self.serailizer_to_use(instance, data = input_data_item, partial=True)
            self.updated_elements += 1
        else:
            serializer = self.serailizer_to_use(data = input_data_item)
            self.created_elements += 1

        serializer.is_valid(raise_exception=True)
        serializer.save()


    def post(self, request, *args, **kwargs):

        input_data = request.data
        if type(input_data) == dict:
            input_data = list(input_data)

        for input_data_item in input_data:
            try:
                instance = self.get_instance(input_data_item)
                self.create_or_update(instance, input_data_item)
            except Exception as err:
                self.raised_exceptions.append(err)

        return Response(self.get_response)

