from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from shop2.category.models import Category
from django.db import models
from shop2.detail.models import Detail
from shop2.files.models import FilesStorage
from shop2.price.models import Price
from shop2.balance.models import Balance


class Product(AbstractGenericModel, FilesStorage):

    link = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    product_code = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, default="Описания нет")
    unit_of_measurement = models.CharField(max_length=15)
    products_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    details = models.ManyToManyField(Detail)
    view_in_catalog = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_price(self):
        price_instance = Price.objects.filter(product=self).first()
        if price_instance:
            return f'{str(price_instance.value)} {price_instance.currency}/{self.unit_of_measurement}'
        else:
            return 'цена по запросу'
        

    def get_balance(self):
        balance_instance = Balance.objects.filter(product=self).first()
        if balance_instance:
            return f'На складе {str(balance_instance.value)} {self.unit_of_measurement}'
        else:
            return 'Нет данных по остаткам'