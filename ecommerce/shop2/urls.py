from shop2.category.urls import urlpatterns as categories_urls
from shop2.product.urls import urlpatterns as products_urls
from shop2.detail.urls import urlpatterns as detail_urls
from shop2.files.urls import urlpatterns as files_urls
from shop2.filter_catalog.urls import urlpatterns as filter_urls
from shop2.price.urls import urlpatterns as prices_urls
from shop2.balance.urls import urlpatterns as balances_urls

app_name = "shop2"

urlpatterns = [
    *categories_urls,
    *products_urls,
    *detail_urls,
    *files_urls,
    *filter_urls,
    *prices_urls,
    *balances_urls,
]