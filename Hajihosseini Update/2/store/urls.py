# ********************************************************************************************************
# from django.urls import path

# from . import views_functional as views

# urlpatterns = [
#     path('', views.home_page, name='home'),
#     path('products/', views.product_list, name='product_list'),
#     path('products/<int:pk>', views.product_detail, name='product_detail'),
#     path('categories/', views.category_list, name='category_list'),
#     path('categories/<int:pk>', views.category_detail, name='category_detail'),
#     path('discounts/', views.discount_list, name='discount_list'),
#     path('discounts/<int:pk>', views.discount_detail, name='discount_detail'),
# ]
# ********************************************************************************************************


# ********************************************************************************************************
# from django.urls import path

# from . import views_class_based_1 as views
# from . import views_class_based_2 as views

# urlpatterns = [
#     path('', views.HomePage.as_view(), name='home'),
#     path('products/', views.ProductList.as_view(), name='product_list'),
#     path('products/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
#     path('categories/', views.CategoryList.as_view(), name='category_list'),
#     path('categories/<int:pk>', views.CategoryDetail.as_view(), name='category_detail'),
#     path('discounts/', views.DiscountList.as_view(), name='discount_list'),
#     path('discounts/<int:pk>', views.DiscountDetail.as_view(), name='discount_detail'),
# ]
# ********************************************************************************************************


# ********************************************************************************************************
# from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
# # دیفالت میاد صفحه اولیه هم که همه لینک ها رو داره درست میکنه

# from . import views

# router = DefaultRouter()
# router.register('products', views.ProductViewSet, basename='product') # => product-list | product-detail
# router.register('categories', views.CategoryViewSet, basename='category') # => category-list | category-detail
# router.register('discounts', views.DiscountViewSet, basename='discount') # => discount-list | discount-detail
# router.register('comments', views.CommentViewSet, basename='comment') # => comment-list | comment-detail
# # urlpatterns = router.urls
# urlpatterns = [
#     path('', include(router.urls)),
# ]
# ********************************************************************************************************


# ********************************************************************************************************
from django.urls import path, include
# برای این که بتونیم به صورت نستد هم نشون بدیم. مثلا تو محصولات هستیم بریم تو محصول ۲۵۴
# اونجا بریم تو قسمت کامنت هاش و اونجا بریم سراغ کامنت ۵۴
# از پکیج نستد رَونتر استفاده میکنیم.
# pip install drf-nested-routers
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product') # => product-list | product-detail
router.register('categories', views.CategoryViewSet, basename='category') # => category-list | category-detail
router.register('discounts', views.DiscountViewSet, basename='discount') # => discount-list | discount-detail
products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')
router.register('carts', views.CartViewSet, basename='cart') # => cart-list | cart-detail
cart_items_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')
# urlpatterns = router.urls + products_router.urls + cart_items_router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(cart_items_router.urls)),
]
