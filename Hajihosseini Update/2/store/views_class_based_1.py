from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Category, Discount, Product
from .serializers2 import CategorySerializer, DiscountSerializer, ProductSerializer


def printype(s):
    print(s, type(s))


class HomePage(APIView):
    def get(self, request):
        return Response('Hi')


class ProductList(APIView):
    def get(self, request):
        query_set = Product.objects.all().select_related('category').order_by('id')
        serializer = ProductSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        # serializer = ProductSerializer(product)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    def put(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count()>0:
            return Response({'error': 'This product is in some order items. Delete them first and then come back😊'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    def get(self, request):
        query_set = Category.objects.all().annotate(products_count=Count('products'))
        serializer = CategorySerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    def put(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
        num_of_products = category.products.count()
        word = 'product' if num_of_products==1 else 'products'
        if num_of_products>0:
            return Response({'error': 'This category has %s %s. Delete them first and then come back😊' %(num_of_products, word)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscountList(APIView):
    def get(self, request):
        query_set = Discount.objects.all()
        serializer = DiscountSerializer(query_set, many=True)
        return Response(serializer.data)


class DiscountDetail(APIView):
    def get(self, request, pk):
        discount = get_object_or_404(Discount, pk=pk)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)
