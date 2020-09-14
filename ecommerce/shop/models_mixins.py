from django.db import models

class GeneralFieldsMixin(models.Model):

    class Meta:
        abstract=True

    active_object = models.BooleanField(default=True)