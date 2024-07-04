from decimal import Decimal
from rest_framework import serializers

from .models import Category, Product


TAX_RATE = Decimal(1.10)


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.ModelSerializer):
    remained = serializers.IntegerField(source='inventory')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_after_tax = serializers.SerializerMethodField() # اسم متغیر کامپیوتد فیلد که به دلخواه خودمون
    # هست. اما برای محاسبه اش به دنبال تابعی هم نام با کامپیوتد فیلد ما میگرده که اولش گیت آندراسکور
    # باشه. که پایین نوشتم. اگه نخوایم اسمش اون باشه، میتونیم داخل سریالایزرمتد فیلد یه اتریبیوت به اسم
    # method_name بهش بدیم و هر اسمی که خودمون دوست داریم به تابع بدیم. اما من دیگه نذاشتم و فقط
    # توضیحش رو همینجا نوشتم که اگه لازم شد این کار رو بکنم. فقط حواسم باشه که اسم متد رو باید 
    # داخل کوتیشن بذاریم. یعنی استرینگِ اسمش رو باید بدیم.
    category = CategorySerializer()

    class Meta:
        model=Product
        fields = ['id', 'name', 'inventory', 'remained', 'price', 'price_after_tax', 'category']
        # fields = '__all__' # هیچ وقت از آل استفاده نکنیم. چون فردا اگه یه فیلد اضافه بشه که
        # فارین کی باشه، آل میخواد اون رو هم بگیره که کلی طول میکشه و همون قضیه ۱۰۰۰ بار هیت
        # پیش میاد که اگه دو لایه باشه میشه ۱۰۰۰ تا ۱۰۰۰ بار که میشه ۱۰۰۰۰۰۰ بار که فاجعه است.
        # جدا از اون مشخص باشه که چی ها رو بدیم بهتره. شاید حالا کوئری هاش زیاد نشه اما ما نخوایم
        # یه فیلد رو بدیم و این طوری به اشتباه بفرستیم.
        # exclude استفاده از
        # exclude = ['datetime_created', 'datetime_modified', 'discounts', 'slug']

    def get_price_after_tax(self, product: Product):
        return round(product.unit_price*TAX_RATE, 2)


class DiscountSerializer(serializers.Serializer):
    discount = serializers.FloatField()
    description = serializers.CharField(max_length=255)