from decimal import Decimal
from django.utils.text import slugify
from django.db import transaction
from rest_framework import serializers

from .models import Cart, CartItem, Category, Comment, Customer, Order, OrderItem, Product, Discount


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


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context.get('cart_pk')
        product=validated_data.get('product')
        quantity=validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        self.instance = cart_item # این خط برای حرفه ای تر بودن هست و خودش از تو داکیومنتیشن جنگو خوونده بود. منم فعلا بذارم ایشالله بعدا متوجه میشم😊
        return cart_item


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total_price']

    product=CartProductSerializer()
    item_total_price=serializers.SerializerMethodField()

    def get_item_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']
    
    items=CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        # s = 0
        # for item in cart.items.all():
        #     item: CartItem
        #     t = item.product.unit_price * item.quantity
        #     s+=t
        # return s
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    # id = serializers.UUIDField(read_only=True) # به جای این که تعریف کنیم دوباره و رید آنلی کنیم میشه تو 
    # متغیر رید آنلی فیلدز کلاس متا نوشت این رو.


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'birth_date']
        read_only_fields = ['user'] # برای این که موقع تغییر اطلاعات کاربری مثل شماره تلفن و یا تاریخ
        # تولد، اشتباها یوزرنیم رو عوض نکنه طرف.
        # البته اگر بخواد بکنه هم به خاطر یک به یک بودن رابطه کاستومر و یوزر بهش ارور میده.
        # اما خب چه کاریه که الکی بی دقتی کنیم. کد رو درست بنویسم از اول که تو شرایط خاص به مشکل نخوره.
        # مثلا اگه یوزری از اول وجود داشته که به هیچ کاستومری وصل نیست. بعد میشه اینجا کاستومر رو
        # تغییر داد. خلاصه این که مشکلی نذاریم که ذهن آدم های مریض انگولک بشه که خرابکاری بکنن.





class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'purchased_price']

    product = OrderItemProductSerializer()
    purchased_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')


class OrderCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']
    
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')
    email = serializers.CharField(max_length=255, source='user.email')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'datetime_created', 'status', 'items']
    
    items = OrderItemSerializer(many=True)


class OrderForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'datetime_created', 'status', 'items']
    
    customer = OrderCustomerSerializer()
    items = OrderItemSerializer(many=True)


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    @transaction.atomic()
    def save(self, **kwargs):
        cart_id = self.validated_data.get('cart_id')
        user_id = self.context.get('user_id')
        customer = Customer.objects.get(user_id=user_id)

        order = Order()
        order.customer = customer
        order.save()
        cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem()
            order_item.order=order
            order_item.product_id=cart_item.product_id # برای این که آبجکت ها رو هی پاس ندیم سنگین نشه، آی دی هاشونو فقط دادیم
            order_item.quantity=cart_item.quantity
            order_item.unit_price=cart_item.product.unit_price
            order_items.append(order_item)
        # به جای این که دونه دونه تابع سیو رو روی هر کودوم از اردرآیتم ها صدا کنیم، همه رو 
        # ریختیم داخل یه لیست و آخر سر از تابع بالک کریت منیجر استفاده کردیم که به جای ۱۰ تا یا ۲۰
        # تا درخواست، همه رو با یه درخواست به دیتابیس میگه.

        # اگه دوست داشتیم، میشه با لیست کامپرهنشن هم این شکلی درستش کرد.
        # order_items=[
        #     OrderItem(
        #         order=order,
        #         product=cart_item.product,
        #         unit_price=cart_item.product.unit_price,
        #         quantity=cart_item.quantity
        #     ) for cart_item in cart_items
        # ]

        OrderItem.objects.bulk_create(order_items)
        Cart.objects.get(id=cart_id).delete()
        return order

    # برای ولیدیت کردن یک فیلد خاص از سریالایزری که میسازیم، تابعی باید بنویسیم که با ولیدیت
    # شروع بشه و یه آندراسکور بذاریم و بعدش اسم فیلد رو بنویسیم. الان ما میخوایم بررسی کنیم که
    # یه سبد خرید خالی نباشه. پس میخوایم ولیدیتش کنیم. پس این تابع رو نوشتیم.
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('There is no cart with cart id %s' %cart_id)
        # اگه وجود نداشت که ارور دادیم بهش. اگه وجود داشت باید ببینیم داخلش آیتم هست یا نه
        if CartItem.objects.filter(cart_id=cart_id).count==0:
            raise serializers.ValidationError('Your cart is empty. Please add some products first!')
        # اگه خالی بود که ارور دادیم بهش. اگه نه که سبد خرید اوکی هست و یه خریدی هم کرده
        return cart_id
        # تعداد کوئری ها این جا دو تاست تو این حالت. اما بهترش میکنیم و تو پایینی با یه کوئری مینویسیم
        # البته تو پایینی هم پریفچ ریلیتد باعث میشه ۲ تا کوئری داشته باشیم. اما کلا یه کوئری اینجا
        # براش نوشتیم و روی کارت فقط کار کردیم. به هر حال هر کودوم یه روش هست دیگه.

    def validate_cart_id(self, cart_id):
        try:
            if Cart.objects.prefetch_related('items').get(id=cart_id).items.count() == 0:
                raise serializers.ValidationError('Your cart is empty. Please add some products first!')
        except Cart.DoesNotExist:
            raise serializers.ValidationError('There is no cart with cart id %s' %cart_id)
        return cart_id

