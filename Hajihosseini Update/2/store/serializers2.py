from decimal import Decimal
from django.utils.text import slugify
from rest_framework import serializers

from .models import Category, Comment, Product, Discount


TAX_RATE = Decimal(1.10)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'num_of_products']
    
    num_of_products = serializers.SerializerMethodField(read_only=True)

    def get_num_of_products(self, category:Category):
        # return category.products.count() # توضیحات کامل رو تو فایل ویوز.پای قسمت مربوطه بخوونم.
        # return category.products_count
        # اما نکته ای که داره اینه که موقعی که یه کتگوری میسازیم، ساختنش تو دیتابیس انجام میشه
        # با این حال به ما ارور میده که
        # 'Category' object has no attribute 'products_count'
        # حتی با این که ما تو جیسون نفرستیم این رو. دلیلش اینه که موقع پست، بعد از ذخیره کردن بهش
        # گفتیم که بیا سریالایزر.دیتا رو نشون بده که خب برای نمایشش، میاد اطلاعات رو بگیره که اینور
        # بهش گفتیم پروداکتس کَونت رو بهش بده. اما موقعی که متد گت نیست، احتمالا نمیاد سریالایزر
        # رو مطابق چیزی که تو این کلاس کتگوری سریالایزر ما بهش گفتیم و فیلدز رو بهش دادیم
        # درست کنه. به خاطر همین به مشکل میخوره. حالا دلیلش خیلی مهم نیست اما با ترای و اکسپت
        # حلش میکنیم. میگیم سعی کن که اون رو بدی که یه هیت کمتر به دیتابیس بزنی. اگه مثل حالت
        # عادی شد که خوبه. اما اگه نشد میگیم یه کوئری دیگه بزن برو تعدادش رو هم بگیر و بعد بیا
        # بهمون نشون بده به اسم همین نام آو پروداکتز یعنی این شکلی میشه کدها
        try:
            return category.products_count
        except AttributeError:
            return category.products.count()



class ProductSerializer(serializers.ModelSerializer):
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

    remained = serializers.IntegerField(source='inventory', read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_after_tax = serializers.SerializerMethodField() # اسم متغیر کامپیوتد فیلد که به دلخواه خودمون
    # هست. اما برای محاسبه اش به دنبال تابعی هم نام با کامپیوتد فیلد ما میگرده که اولش گیت آندراسکور
    # باشه. که پایین نوشتم. اگه نخوایم اسمش اون باشه، میتونیم داخل سریالایزرمتد فیلد یه اتریبیوت به اسم
    # method_name بهش بدیم و هر اسمی که خودمون دوست داریم به تابع بدیم. اما من دیگه نذاشتم و فقط
    # توضیحش رو همینجا نوشتم که اگه لازم شد این کار رو بکنم. فقط حواسم باشه که اسم متد رو باید 
    # داخل کوتیشن بذاریم. یعنی استرینگِ اسمش رو باید بدیم.
    # category = CategorySerializer()

    def get_price_after_tax(self, product: Product):
        return round(product.unit_price*TAX_RATE, 2)
    
    # custom validation
    def validate(self, data):
        # داخل تابع ولیدیت با اسم هایی که ما گذاشتیم کار نداره. با اسم های اصلی تو دیتابیس
        # کار میکنه. مثلا اینجا میخوایم که قیمت رو کمتر از ۵ دلار کسی نده
        if data['unit_price']<5:
            raise serializers.ValidationError("Product price should be greater than or equal to 5!")
        if data['unit_price']>1050:
            raise serializers.ValidationError("Product price should be less than or equal to 1050!")
        if len(data['name'])<2:
            raise serializers.ValidationError("You should enter a real name for your product. No word in english has a length less than 2. الکی نیست که داداچ😁")
        return data
    
    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product
    
    # یه نمونه صرفا جهت این که داشته باشیم آپدیت چه طور کار میکنه. در واقع کار که میکنه خودش
    # اما اگه بخوایم کاستومایزش کنیم. خودش هم حتی تست نکرد فقط نوشت.
    # def update(self, instance: Product, validated_data):
    #     instance.name = validated_data.get('name')
    #     instance.inventory = validated_data.get('inventory')
    #     ...
    #     instance.save()
    #     return instance


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['discount', 'description']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']
    
    def create(self, validated_data):
        product_id = self.context.get('product_pk')
        return Comment.objects.create(product_id=product_id, **validated_data)