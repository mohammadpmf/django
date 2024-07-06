from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Category, Discount, Product
from .serializers2 import CategorySerializer, DiscountSerializer, ProductSerializer


def printype(s):
    print(s, type(s))


class HomePage(APIView):
    def get(self, request):
        return Response('Hi')

class ProductList(ListCreateAPIView):
    # def get_serializer_class(self):
    #     return ProductSerializer
    # def get_queryset(self):
    #     return Product.objects.all().select_related('category').order_by('id')
    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related('category').order_by('id')
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category')

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count()>0:
            return Response({'error': 'This product is in some order items. Delete them first and then come back😊'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().annotate(products_count=Count('products'))


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(products_count=Count('products'))

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
        num_of_products = category.products.count()
        word = 'product' if num_of_products==1 else 'products'
        if num_of_products>0:
            return Response({'error': 'This category has %s %s. Delete them first and then come back😊' %(num_of_products, word)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscountList(ListCreateAPIView):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()


class DiscountDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
