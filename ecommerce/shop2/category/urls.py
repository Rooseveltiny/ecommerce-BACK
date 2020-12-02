from django.urls import path
from shop2.category.views import LoadCategoryView

urlpatterns = [
    path('load_categories', LoadCategoryView.as_view())
]