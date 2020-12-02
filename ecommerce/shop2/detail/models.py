from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from shop2.product.models import Product
from django.db import models


class DetailGroup(AbstractGenericModel):

    link = models.UUIDField(default=uuid4, null=False, editable=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, null=True, unique=True)


class Detail(AbstractGenericModel):

    link = models.UUIDField(default=uuid4, primary_key=True, null=False, editable=True)
    title = models.CharField(max_length=200)
    detail_group = models.ForeignKey(DetailGroup, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, null=True, unique=True)
