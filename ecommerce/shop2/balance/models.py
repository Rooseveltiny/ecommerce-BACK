from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from django.db import models


class Balance(AbstractGenericModel):

    id = models.AutoField(primary_key=True)
    value = models.DecimalField(
        max_digits=15, decimal_places=3, default=0)
    place = models.CharField(max_length=200, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    