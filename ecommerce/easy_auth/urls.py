from django.urls import path, include
from easy_auth import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('restricted/', views.restricted),
    path('email/change', views.Email.as_view)
]