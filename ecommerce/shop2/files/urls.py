from django.urls import path
from shop2.files.views import LoadFilesView

urlpatterns = [
    path('load_files', LoadFilesView.as_view())
]