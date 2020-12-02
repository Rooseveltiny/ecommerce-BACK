from django.urls import path
from shop2.detail.views import LoadDetailGroupsView, LoadDetailView

urlpatterns = [
    path('load_detail_groups', LoadDetailGroupsView.as_view()),
    path('load_detail', LoadDetailView.as_view())
]