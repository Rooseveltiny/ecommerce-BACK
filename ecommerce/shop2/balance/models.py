from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from shop2.product.models import Product
from django.db import models


class Balance(AbstractGenericModel):

    link = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    value = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    place = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    