from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from django.db import models

class Price(AbstractGenericModel):

    price_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    value = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=50)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)