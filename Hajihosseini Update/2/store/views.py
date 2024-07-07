from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Comment, Discount, Product
from .serializers2 import CategorySerializer, CommentSerializer, DiscountSerializer, ProductSerializer
from .filters import ProductFilter
from .paginations import ProductPagination

def printype(s):
    print(s, type(s))


class HomePage(APIView):
    def get(self, request):
        return Response('Hi')


# اگه بخوایم توانایی تغییر نداشته باشه و فقط بتونه بخونه اطلاعات رو، از رید آنلی مدل ویو ست استفاده
# میکنیم. یعنی این رو ایمپورت میکنیم از همونجایی که مدل ویو ست رو آوردیم و از این ارث بری میکنیم
# ReadOnlyModelViewSet
# این طوری دیگه کارهای تغییرش وجود ندارند و فقط برای ما لیست ویو و دیتیل ویو رو میاره.
# برای تخفیف ها که خودش نذاشته بود و خودم اضافه گذاشته بودم این رو گذاشتم. یعنی تخفیف ها رو فقط
# الان میشه دید. ویرایش و حذف و ایجاد ندارن.
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related('category').order_by('id')
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['name', 'unit_price', 'inventory']
    search_fields = ['name', 'category__title']
    # filterset_fields = ['category', 'inventory']
    filterset_class = ProductFilter
    # برای پجینیشن، اگه تو ستینگز و داخل دیکشنری رست فریم ورک اونا رو اضافه کنیم، برای همه اعمال
    # میشه و لازم نیست کاری بکنیم. اما میتونیم اینجا متغیر زیر رو تعریف کنیم و وصلش کنیم به کد
    # خودمون که برای هر ویویی جدا باشه. این شکلی اینجا نوشتم و داخل فایل پجینیشنز.پای کلاسش رو
    pagination_class = ProductPagination
    # حتی میشه تو ستینگز دیفالت رو هم گذاشت و برای هر ویویی، پجینیشن جداگانه هم تعریف کرد که اگه
    # جایی نگفتیم از دیفالت استفاده کنه و اگه گفتیم از مال ما.
    
    # این کوئری ست که پایین نوشتم، برای اینه که بر اساس چیزهای خاص فیلتر کنیم. اما خودمون
    # بخوایم همه چیز رو بنویسیم پیر میشیم. با دستور pip install django-filter
    # پکیجش رو نصب میکنیم و ازش استفاده میکنیم (یادم نره تو ستینگز هم django_filters رو قبل از
    # rest_framework اضافه کنم که بشناستش) این طوری دیگه لازم نیست دوباره برای کوئری ست تابع تعریف کنیم
    # و همون متغیر queryset کافی هست. فقط چند تا متغیر ساده دیگه هم باید تعریف کنیم که بالا نوشتم 
    # def get_queryset(self):
    #     query_set = Product.objects.all()
    #     category_id_parameter = self.request.query_params.get('category_id')
    #     if category_id_parameter:
    #         query_set = query_set.filter(category_id=category_id_parameter)
    #     return query_set

    
    def get_serializer_context(self):
        return {'request': self.request}

    # فرقش با قبلی اینه که اینجا اسمش رو باید دیستروی بذاریم به جای دیلیت
    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count()>0:
            return Response({'error': 'This product is in some order items. Delete them first and then come back😊'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().annotate(products_count=Count('products'))

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
        num_of_products = category.products.count()
        word = 'product' if num_of_products==1 else 'products'
        if num_of_products>0:
            return Response({'error': 'This category has %s %s. Delete them first and then come back😊' %(num_of_products, word)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscountViewSet(ReadOnlyModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk') # از کجا میدونیم وجود داره؟
        # خودمون توی یو آر الز بهش گفتیم که لوکاپ = پروداکت باشه. پس برامون پروداکت آندراسکور پی کی
        # رو میفرسته.
        return Comment.objects.filter(product_id=product_pk)
    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs.get('product_pk')}