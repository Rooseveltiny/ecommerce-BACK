from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from ecommerce import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/base-auth', include('rest_framework.urls')),
    path('api/v1/shop/', include('shop.urls')),
    path('api/v2/shop/', include('shop2.urls')),
    path('auth/', include('easy_auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
