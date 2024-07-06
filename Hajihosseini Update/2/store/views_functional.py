from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Category, Discount, Product
from .serializers2 import CategorySerializer, DiscountSerializer, ProductSerializer


def printype(s):
    print(s, type(s))


@api_view()
def home_page(request):
    return Response('Hi')


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method=='GET':
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
    elif request.method=='POST':
        serializer = ProductSerializer(data=request.data)
        # روش ۱
        # که استفاده نمیکنیم هیچ وقت
        # if serializer.is_valid():
        #     pass
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # روش ۲
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    # جهت بهینه کردن کد و کمتر هیت زدن به دیتابیس موقع گرفتن جزییات یک محصول کد رو اصلاح کردیم.
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    if request.method=='GET':
        # serializer = ProductSerializer(product)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.order_items.count()>0:
            return Response({'error': 'This product is in some order items. Delete them first and then come back😊'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method=='GET':
        # query_set = Category.objects.all().prefetch_related('products')
        # این خوبه. ولی بعدی بهتره تو خود تیبل اولیه هم متغیری به اسم پروداکت کَونت اضافه میکنه
        # و اون رو میگیریم. فقط دقت کنم که تو تابعی که تو سریالایزر نوشتم دوباره نیام از منیجرش
        # پروداکتس رو بگیرم بعد متد کَونت رو صدا کنم. اون طوری دوباره همه رو میگیره و تعداد هیت به
        # دیتابیس زیاد میشه. اگه پریفچ ریلیتد هم بذارم تعداد هیت کم میشه. اما خب دیگه کار انوتیتی که ما
        # گذاشتیم بی فایده میشه. خلاصه این که اگه کوئری بالایی رو نوشتم خوب هست. اما تو تابع سریالایزرمون
        # که نوشتیم باید بنویسم
        # category.products.count()
        # و اگه پریفچ ریلیتد اینجا نباشه کلی هیت به دیتابیس میزنه. اما وقتی هست ۲ تا هیت میزنه
        # ولی اگه کوئری پایین رو بنویسیم و تو تابع سریالایزرمون هم بنویسیم
        # category.products_count
        # این طوری کلا فقط ۱ هیت به دیتابیس میزنه.
        # و تاکید مجدد که اگه کوئری پایینی رو بزنیم و تو تابع سریالایزر باز هم بنویسیم
        # category.products.count()
        # این به تعداد کتگوری های ما + ۱ هیت به دیتابیس میزنه که خیلی بده.
        # اگه رو کوئری زیر هم پریفچ ریلیتد بذاریم که همون ۲ تا هیت میشه دوباره. اما الکی یه
        # فیلد پروداکتس کَونت تعریف کردیم که ازش هیچ استفاده ای نکردیم.
        # نکته آخر هم این که پریفچ واقعا میره همه رو میاره از دیتابیس. حالا فرض کن ۱۰۰۰ تا باشه
        # الکی ما اطلاعات ۱۰۰۰ تا محصول که شاید ۱۰۰ کیلوبایت بشه رو هم از دیتابیس گرفتیم
        # در حالی که فقط تعدادشون رو میخواستیم. درسته که دیتابیس سریع هست و این که ۱ یا ۲ هیت
        # بهش بزنیم خیلی تفاوتی نکنه. اما دقت کنم که تو سطح اطلاعات بزرگ تفاوت میکنه.
        # وقتی اون لحظه من فقط تعداد محصولات رو به یه دلیلی میخوام. چرا الکی برم کلی اطلاعات
        # هزار تا محصول رو بگیرم که به کارم هم نمیاد و الکی ۱۰۰ کیلوبایت داده بین دیتابیس و 
        # 😁من رد و بدل بشه و رم رو هم الکی پر بکنم؟ عَیب نیست؟
        query_set = Category.objects.all().annotate(products_count=Count('products'))
        serializer = CategorySerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    # همون توضیحات لیست ویو در مورد انوتیت
    category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
    if request.method=='GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        num_of_products = category.products.count()
        word = 'product' if num_of_products==1 else 'products'
        if num_of_products>0:
            return Response({'error': 'This category has %s %s. Delete them first and then come back😊' %(num_of_products, word)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
