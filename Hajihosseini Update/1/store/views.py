from django.shortcuts import render

from .models import Product, Address, Comment, Cart, CartItem, Category, Customer, Discount, OrderItem, Order


def printype(x):
    print(x, type(x))


def show_data(request):
    context = {
        'alaki': 12345
    }
    query_set = Product.objects.all()
    printype(query_set)
    return render(request, 'store/home.html', context)