from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category, Discount, Product
from .serializers import CategorySerializer, DiscountSerializer, ProductSerializer


def printype(s):
    print(s, type(s))


@api_view()
def home_page(request):
    return Response('Hi')


@api_view()
def product_list(request):
    # query_set = Product.objects.all()
    # برای بهبود سرعت سریالایزر باید این کوئری ست رو بهینه کنیم. اما وقتی سلکت ریلیتد میزدم،
    # ترتیبشون عوض میشد و ۱۴ میومد اول و غیره. برای این که به هم نریزه، خودم دوباره بر اساس
    # آی دی محصولات هم گفتم مرتب کنه
    query_set = Product.objects.all().select_related('category').order_by('id')
    # serializer = ProductSerializer(query_set, many=True)
    # این حالت عادی بود. اما برای این که از تو سریالایزر بشه
    # از هایپرلینکد ریلیتد فیلد استفاده بشه، ارور میده میگه که رکوئست رو هم براش باید
    # ارسال میکردیم که به خاطر همین میایم اینجا رکوئست رو هم براش میفرستیم. برای این که تو حالت
    # دیتیل هم بشه لینک رو دید و روش کلیک کرد و همین ارور رو به ما نده، تو دیتیل ویو هم همین
    # کار رو کردم اما دیگه این توضیحات رو اونجا نمینویسم
    serializer = ProductSerializer(query_set, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def product_detail(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    # جهت بهینه کردن کد و کمتر هیت زدن به دیتابیس موقع گرفتن جزییات یک محصول کد رو اصلاح کردیم.
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    # serializer = ProductSerializer(product)
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view()
def discount_list(request):
    query_set = Discount.objects.all()
    serializer = DiscountSerializer(query_set, many=True)
    return Response(serializer.data)


@api_view()
def discount_detail(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    serializer = DiscountSerializer(discount)
    return Response(serializer.data)
