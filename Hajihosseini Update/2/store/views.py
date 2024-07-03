from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer


@api_view()
def home_page(request):
    print('o')
    return Response('Hi')


@api_view()
def product_list(request):
    return Response('List of products')


@api_view()
def product_detail(request, pk):
    return Response(pk)
