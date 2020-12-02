from django.db import models
from datetime import datetime

class AbstractGenericModel(models.Model):

    marked_to_delete = models.BooleanField(default=False)

    class Meta:

        abstract = True