from decimal import Decimal
from rest_framework import serializers

from .models import Category, Product


TAX_RATE = Decimal(1.10)


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    inventory = serializers.IntegerField()
    remained = serializers.IntegerField(source='inventory')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_after_tax = serializers.SerializerMethodField() # اسم متغیر کامپیوتد فیلد که به دلخواه خودمون
    # هست. اما برای محاسبه اش به دنبال تابعی هم نام با کامپیوتد فیلد ما میگرده که اولش گیت آندراسکور
    # باشه. که پایین نوشتم. اگه نخوایم اسمش اون باشه، میتونیم داخل سریالایزرمتد فیلد یه اتریبیوت به اسم
    # method_name بهش بدیم و هر اسمی که خودمون دوست داریم به تابع بدیم. اما من دیگه نذاشتم و فقط
    # توضیحش رو همینجا نوشتم که اگه لازم شد این کار رو بکنم. فقط حواسم باشه که اسم متد رو باید 
    # داخل کوتیشن بذاریم. یعنی استرینگ اسمش رو باید بدیم.

    # ForeignKey باز هم داستان داره.
    # category = serializers.PrimaryKeyRelatedField() # این طوری که ارور میده. میگه باید یا کوئری ست
    # براش تعریف کنی یا رید آنلی رو ترو بذاری
    # روش ۱
    # که به درد نمیخوره. فقط آی دی شو میده
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    # روش ۲
    # کوئری ست تعریف میکنیم براش. که این هم همون آش و همون کاسه است. فقط آی دی شو میده
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # روش ۳
    # اگه بخوایم اسمش رو بنویسه، باید تو کلاس کتگوری تابع اس تی آرش رو نوشته باشیم. تو این حالت
    # میشه به جای پرایمری کی ریلیتد فیلد از استرینگ ریلیتد فیلد استفاده کرد که این کلاس، خودش
    # رید آنلی هست و لازم نیست داخلش بنویسیم رید آنلی مساوی با ترو و اسم همه رو هم میاره
    # اما مشکلش اینه ۱۰۰۰ تا کوئری میزنه و خیلی کند هست. سریالایزر فقط رابط ما هست. برای این
    # که کند نباشه، ما باید توی ویومون کدی رو که نوشتیم اصلاح کنیم و بریم اونجا سلکت ریلیتد
    # رو استفاده کنیم که موقع زدن کوئری اول، خود اطلاعات کتگوری ها رو هم بگیره.
    # فقط حواسم باشه که هم برای لیست ویو اصلاحش کنم هم برای دیتیل ویو که برای دیتیل ویو داخل
    # تابع گت آبجکت اور ۴۰۴ هم میتونیم کوئری بهتر بزنیم. فایل ویوز رو ببینم متوجه میشم. 
    # category = serializers.StringRelatedField()
    # روش ۴
    # استفاده از هایپرلینکد ریلیتد فیلد هست که شاید به نظرم خیلی پرکاربرد نیاد الان و استفاده
    # از سرایالایزرهای تو در تو رو ترجیح بدم. اما فکر کنم تو اِی پی آی های واقعی و کاربردی
    # چیز به درد بخوری باشه. به هر حال دارم مینویسم. در واقع لینک اون چیزی که بهش فارین کی
    # زده شده رو به ما میده. اما ما تو حالت عادی فقط عدد فارین کی رو داریم. پس باید لینکش رو
    # خودمون از رو عدده درست کنیم. برای این کار باید یک تابع براش بنویسیم. مثلا تو فایل ویوز.پای
    # یک تابع به اسم کتگوری دیتیل مینویسیم که جزییات یک کتگوری رو تحویل بده و بعد
    # اینجا بهش وصلش میکنیم مثل کد زیر
    # category = serializers.HyperlinkedRelatedField(
    #     view_name='category_detail',
    #     queryset=Category.objects.all()
    #     )
    # که این ۲ تا ورودی اجباری هست. حالا وقتی صفحه رو لود میکنیم به ما ارور میده و میگه که
    # باید رکوئست رو براش بفرستیم و برای این که کار کنه، رفتیم تو متدهای مربوط به پروداکت موقع
    # ساخت سرایالایزر، رکوئست رو هم بهش دادیم. یه کم سخت بود و خیلی حال نکردم. با این حال
    # نوشتم که داشته باشمش.
    # ⭐⭐⭐👍👍👍💙💙💙 روش ۵ 💚💚💚👍👍👍⭐⭐⭐
    # استفاده از سریالایزرهای تو در تو هست که هم خیلی قشنگ و عالی هست و هم کاربردی و چیزی
    # که تو دنیای اِی پی آی ها بینهایت استفاده میشه. فقط دقت کنم که تعداد کوئری ها مثل همون
    # استرینگ ریلیتد فیلد هست و ما باید اون ور تو ویوز.پای کوئری مون رو بهینه کنیم تا این هم
    # 👍 سریع باشه. اما نحوه نمایشش عالیه و خودم این رو ترجیح میدم نحوه نوشتنش هم خیلی آسونه 👍
    category = CategorySerializer()

    def get_price_after_tax(self, product: Product):
        return round(product.unit_price*TAX_RATE, 2)


class DiscountSerializer(serializers.Serializer):
    discount = serializers.FloatField()
    description = serializers.CharField(max_length=255)