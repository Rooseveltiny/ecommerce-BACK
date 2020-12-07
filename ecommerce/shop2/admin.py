from django.contrib import admin
from shop2.product.models import Product
from shop2.category.models import Category

to_register = (Product, Category, )
[admin.site.register(model) for model in to_register]