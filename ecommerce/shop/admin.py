from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Detail)
admin.site.register(DetailGroup)
admin.site.register(Product)
admin.site.register(Category)