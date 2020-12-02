from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from shop2.category.models import Category
from django.db import models

class Product(AbstractGenericModel):

    link = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    product_code = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, default="Описания нет")
    unit_of_measurement = models.CharField(max_length=15)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.title