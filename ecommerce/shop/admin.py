from django.contrib import admin

# Register your models here.

from .models import Detail, DetailGroup, Product

admin.site.register(Detail)
admin.site.register(DetailGroup)
admin.site.register(Product)