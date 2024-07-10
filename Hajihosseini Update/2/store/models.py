from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    def __str__(self):
        return f"{self.title}"


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.discount} | {self.description}"

    

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(Discount, blank=True)

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)


class OrderManager(models.Manager):
    def get_by_status(self, status):
        return self.get_queryset().filter(status=status)


class UnpaidOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)

    my_manager = OrderManager()
    unpaid_manager = UnpaidOrderManager()
    objects = models.Manager()
    # حالت عادی لازم نیست بنویسیم. اما وقتی حداقل یه منیجر تعریف میکنیم (که من اینجا دو تا تعریف کردم)، تو این
    # حالت دیگه objects رو نمیشناسه. اونور نوشته بودم ارور داد. اما چون دیگه به همون کلمه objects عادت کردم،
    # گفتم بیام یه دونه objects هم تعریف کنم که اذیتم نکنه. هر چند که my_manager هم تمام اون کارها رو 
    # به علاوه کاری که ما اضافه کردیم انجام میده، اما به هر حال اسمش objects نیست 😁


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = [['order', 'product']]


class CommentManager(models.Manager):
    def get_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)

    def get_not_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_NOT_APPROVED)
        
    def get_waiting(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_WAITING)


class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)
    

class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    my_objects = CommentManager()
    approved_objects=ApprovedCommentManager()
    objects = models.Manager()
    # حالت عادی لازم نیست بنویسیم. اما وقتی حداقل یه منیجر تعریف میکنیم (که من اینجا دو تا تعریف کردم)، تو این
    # حالت دیگه objects رو نمیشناسه. اونور نوشته بودم ارور داد. اما چون دیگه به همون کلمه objects عادت کردم،
    # گفتم بیام یه دونه objects هم تعریف کنم که اذیتم نکنه. هر چند که my_objects هم تمام اون کارها رو 
    # به علاوه کارهایی که ما اضافه کردیم انجام میده، اما به هر حال اسمش objects نیست 😁


from uuid import uuid4
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]




# https://docs.djangoproject.com/en/5.0/howto/custom-lookups/
# برای اضافه کردن لوکاپ کاستومایز شده خودمون، نوشته بود که باید قبل از این که ازش استفاده بشه تعریفش کنیم.
# تو کدهای ویوز، قبل از استفاده تعریف کردم این ها رو و کار میکرد.
# اما اصولیش که تو سایت جنگو و لینکی که گذاشتم نوشته بود اینه که یا تو فایل مدلز بذاریم که من
# همینجا گذاشتم و دیدم کار میکنه و درست هم هست. یا این که تو فایل اپس د اخل
# AppConfig که تو این پروژه میشه فایل اپس و کلاس StoreConfig
# داخل تابع ready اون کلاس رجیسترش کنیم که وقتی من نوشتم
# def ready خود وی اس کد کمک کرد و اونجا هم نوشتم کار کرد. اما به نظرم اینجا خیلی راحت تر و سرراست تره.
# خلاصه این مثال اول سایتشون بود که نوشتم و برای بررسی اینه که بتونیم با لوکاپی به اسم ne
# چیزهایی که دقیقا مخالف با چیز مد نظر ما هستند رو بگیریم. مثلا name__ne="Ali"
# رو اگه رو کامنت ها بزنیم، کامنت هایی رو میاره که اسم طرف علی نباشه.
# مثال جالبی بود گذاشتم باشه. حالا خودم هم میخوام لوکاپ خودم رو بنویسم.
from django.db.models import Lookup
from django.db.models import Field


@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s <> %s" % (lhs, rhs), params
        return f"{lhs} <> {rhs}", params # این هم خودم تغییر دادم و کار میکرد. اما شاید مشکل اس کیو ال اینجکشن داشته باشه


@Field.register_lookup
class LengthLessThan(Lookup):
    lookup_name = "length_less_than"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        print(100*'-')
        print(lhs) # فهمیدم که لفت هند سایت میاد اسم تیبل و اون ستون خاص رو مینویسه
        print(lhs_params) # یه لیست خالی بود. احتمال زیاد همیشه این طور نیست 😊
        print(100*'-')
        print(rhs) # یه درصد اس نوشته بود. چون یه وردی لوکاپ بهش داده بودم. شاید بیشتر بدیم ۲ ۳ تا درصد اس بشه. اما گفتم الکی وقتم رو نگیرم لازم شد یاد میگیرم همون موقع
        print(100*'-')
        print(rhs_params) # یه لیست بود که مقدار استرینگی که مساوی گذاشته بودم یعنی تو مثال من ۱۰۰ رو داده بود.
        params = lhs_params + rhs_params
        return "LENGTH(%s) < %s" % (lhs, rhs), params
    