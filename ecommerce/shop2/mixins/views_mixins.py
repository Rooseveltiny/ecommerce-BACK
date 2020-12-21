from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from shop2.mixins.serailizers_mixins import AbstractLoadingSerializer


class AbstractLoadingView(APIView):

    look_fields = ('link',)
    serailizer_to_use = None
    models_to_use = None

    updated_elements = 0
    created_elements = 0
    raised_exceptions = []

    def __init__(self, *args, **kwargs):

        serailizer = AbstractLoadingSerializer
        serailizer.Meta.model = self.models_to_use
        self.serailizer_to_use = serailizer

        self.updated_elements = 0
        self.created_elements = 0
        self.raised_exceptions = []

    @property
    def get_response(self):
        result = f'Создано элементов: {self.created_elements}. Обновлено элементов: {self.updated_elements}.'
        if len(self.raised_exceptions):
            result = f'{result}  Ошибки: {self.raised_exceptions}'
        return result

    def get_instance(self, input_data_item):

        query_instance = self.models_to_use.objects.all()
        for search_el in self.look_fields:
            searching_kwargs = {search_el: input_data_item[search_el]}
            query_instance = query_instance.filter(**searching_kwargs)
        return query_instance.first()

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

