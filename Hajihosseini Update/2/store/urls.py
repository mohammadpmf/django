from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>', views.product_detail, name='product_detail'),
    path('categories/<int:pk>', views.category_detail, name='category_detail'),
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/<int:pk>', views.discount_detail, name='discount_detail'),
]
