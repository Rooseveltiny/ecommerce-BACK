from shop2.category.urls import urlpatterns as categories_urls
from shop2.product.urls import urlpatterns as products_urls
from shop2.detail.urls import urlpatterns as detail_urls

app_name = "shop2"

urlpatterns = [
    *categories_urls,
    *products_urls,
    *detail_urls
]