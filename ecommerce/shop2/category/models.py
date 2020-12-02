from shop2.mixins.models_mixins import AbstractGenericModel
from uuid import uuid4
from django.db import models

class Category(AbstractGenericModel):

    link = models.UUIDField(default=uuid4, null=False, primary_key=True, editable=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    parent = models.UUIDField(null=True)

    
