from django.shortcuts import render
from rest_framework import generics
from shop.serializers import ProductsListSerializer, ProductSerializer
from shop.models import Product

# Create your views here.

class ProductsListView(generics.ListAPIView):

    serializer_class = ProductsListSerializer
    queryset = Product.objects.all()

class ProductView(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

