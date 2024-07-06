from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Category, Discount, Product
from .serializers2 import CategorySerializer, DiscountSerializer, ProductSerializer


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
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related('category').order_by('id')
    
    def get_serializer_context(self):
        return {'request': self.request}

    # فرقش با قبلی اینه که اینجا اسمش رو باید دیستروی بذاریم به جای دیلیت
    def delete(self, request, pk):
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
