from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

@api_view()
def home_page(request):
    print('o')
    return Response('Hi')


@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    print(serializer)
    print(serializer.data)
    return Response(serializer.data)
