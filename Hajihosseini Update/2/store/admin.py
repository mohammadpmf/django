from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse

from .models import Product, Address, Comment, Cart, CartItem, Category, Customer, Discount, OrderItem, Order

admin.site.site_header = 'تغییر هدر صفحه اولیه ادمین'
admin.site.index_title = 'تغییر عنوان ایندکس صفحه اولیه ادمین'


# این برای کاستوم فیلتر هست. اول برم کلاس های بعدی جایی که لازم شد برگردم به این
class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_AND_10 = '3<=10'
    MORE_THAN_10 = '>10'
    # MORE_THAN_10 = 'ziad' هر چی دلم میخواد. این چیزی هست که تو یو آر ال میفرسته
    title = 'تعداد موجودی در انبار' # عنوانی که تو پنل ادمین مینویسه برای ما
    parameter_name = 'inventory' # این هم اسم کوئری پارامتری هست که با متد گت توی یو آر ال میفرسته. آی دی یا هر چیزی بذاریم مهم نیست. اما بهتره منطقی باشه که اینونتوری هست. اما خلاصه کدی که تو متد گت کوئری ست مینویسیم اجرا میشه و این فقط اسم کوئری پارامتر هست

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'بحرانی'),
            (InventoryFilter.BETWEEN_3_AND_10, 'کمتر از ۱۰ تا'),
            (InventoryFilter.MORE_THAN_10, 'مناسب'),
            # ('الکی', 'هرچیزی همین طوری الکی'), اینا تگ های لینکی هست که تو پنل ادمین برامون میسازه
        ]
    
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_AND_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product_category', 'inventory', 'unit_price', 'inventory_status', 'num_of_comments']
    list_display_links = ['id', 'name', 'inventory', 'inventory_status']
    list_per_page = 50
    list_editable=['unit_price']
    list_select_related = ['category'] # برای تابع پروداکت کتگوری که نوشتیم، باز تعداد زیادی هیت میزنه به دیتابیس که اینجا نحوه نوشتن سلکت ریلیتد این شکلی هست که کمتر هیت بزنه به دیتابیس
    list_filter = ['datetime_created', 'category', InventoryFilter]
    # اگه خودمون بخوایم فیلتر کاستوم بسازیم هم میتونیم و اسم کلاسش رو مینویسیم مثل همین اینونتوری فیلتر
    actions = ['clear_inventory'] # این متد رو خودمون پایین تر داخل کلاس تعریف کردیم
    prepopulated_fields = {
        'slug': ['name', ]
    }
    search_fields = ['name']
    # fields = ['name', 'slug'] # یعنی تو صفحه جزییات که رفتیم فقط اینها رو نشون بده. لیست دیسپلی توی
    # لیست ویو بود. ولی فیلدز توی دیتیل ویو هست. اما دقت کنم که با این دو تا بهم ارور میده
    # چون کلی هاشون نات نال بودند. صرفا نوشتم که باشه و بدونم چیکار میکنه
    # exclude = ['discounts'] # بهش میگیم غیر از این بقیه رو نشون بده. این هم با این که اختیاری هست
    # اما کامنتش میکنم.
    # readonly_fields = ['category'] # این یکی به ما نشون میده اما نمیذاره تغییرش بدیم که خب اینجا باز
    # موقع ساخت ارور میده چون اجباری بود و باید تعیین کنیم. اما موقع ویرایش مشکلی نیست به ما
    # نشون میده چه کتگوی ای داره اما نمیتونیم تغییرش بدیم.

    # به این میگن computed field. فیلدی هست که تو تیبل نیست اما ما میتونیم براش تابع بنویسیم
    # که خودش حساب کنه و تو پنل ادمین به ما نشون بده. اسمی که تو لیست دیسپلی نوشتم باید با اسم
    # تابعی که اینجا مینویسم یکی باشه. انتخاب اسم تابع با خودم هست.
    def inventory_status(self, product: Product):
        if product.inventory==0:
            return 'empty'
        if product.inventory<10:
            return 'low'
        if product.inventory>50:
            return 'high'
        return 'ok'

    # حالا اگه بخوایم تو اردرینگ هم بشه ازش استفاده کرد، یعنی بشه بر اساس این کامپیوتد فیلدی که ما
    # نوشتیم بشه تو صفحه ادمین مرتبشون کرد، از دکوریتور ادمین.دیسپلی استفاده میکنیم که بگیم بر اساس
    # چی سورت کنه وقتی بهش گفتیم بر اساس این مرتب کنه. یعنی بر اساس چه فیلدی ازش. به عنوان مثال
    # تو پایینی ازش استفاده کردم و گفتم که اجازه بده مرتبش کنیم. وقتی زدیم، تو بر اساس کتگوری آی دی
    # ای که داشتن اونها رو مرتب کن به صورت نزولی
    @admin.display(ordering='-category_id')
    # یا مثلا میشه گفت بر اساس تایتل اونها رو مرتب کن صعودی
    # @admin.display(ordering='category__title')
    def product_category(self, product: Product):
        return product.category.title
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments').annotate(comments_count=Count('comments'))

    @admin.display(ordering='comments_count', description='تعداد کامنت ها')
    def num_of_comments(self, product: Product):
        # return product.comments_count
        # return product.comments.count()
    # تا اینجا اوکی هست. میشه کامنت ها رو هم مرتب کرد. حالا میخوایم وقتی مثلا رو ۷ زدیم بره
    # تو پنل ادمین اون ۷ تا کامنت مرتبط رو به ما نشون بده. از تابع فرمت اچ تی ام ال استفاده میکنیم
        url = (
            reverse('admin:store_comment_changelist')
            + '?'
            + urlencode({ # استفاده از یو آر ال انکود به خاطر اینه که کاراکترهای خاص مثل اسپیس و اینا رو خودش مدیریت کنه ما الکی با استرینگ سر و کله نزنیم با استرینگ هم خودم نوشتم کار میکرد اما این اصولی تر، درست تر و بهتره و مال من یه حالت خاص بود. کلی جاها ممکن بود باگ بخوره. اما این خب خیلی بیشتر تست شده هست.
                'product__id': product.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
    
    # ساخت کاستوم اکشن
    # توضیح این که مثلا به صورت پیش فرض تو صفحه اول ادمین فقط دیلیت رو داره.
    # ما میخوایم یه کار خاص بکنیم برای برخی از محصولات. مثلا فروش رفتن تعداد اینونتوری شون رو میخوایم
    # صفر بکنیم یا هر کار دیگه ای این شکلی میسازیم. (اسم دلخواه ورودی این سه تا)
    # و دکوریتور admin.action رو هم اضافه میکنیم
    admin.action(description='خالی کردن اینونتوری محصولات')
    def clear_inventory(self, request, queryset):
        # کوئری ست در واقع میشه مجموعه ای از اعضایی که از اون صفحه انتخاب کردیم. الان مثلا
        # این متد داخل کلاس پروداکت ادمین هست. پس اگه ۴ تا رو تیک زدیم، کوئری ست میشه اون ۴
        # تا محصولی که انتخابشون کردیم. حالا روشون میتونیم متدهای منیجر رو صدا کنیم
        # queryset.update(inventory=0)
        # یادم نره که اول کلاس داخل متغیری به اسم actions باید بنویسیم اسم این متد رو تا اضافه بشه
        # این خط بالا کار میکرد اما پیغامی نمیداد. حالا میخوایم پیغام هم بده. پس از رکوئست هم استفاده
        # میکنیم و براش میفرستیم نتیجه رو. این طوری:
        update_count = queryset.update(inventory=0)
        # self.message_user(request, f"تعداد اینونتوری {update_count} عدد از محصولات به ۰ تغییر کرد.")
        # حالا اگه بخوایم رنگ هم بدیم،
        from django.contrib import messages
        self.message_user(
            request,
            f"تعداد اینونتوری {update_count} عدد از محصولات به ۰ تغییر کرد.",
            messages.WARNING
            )


# class OrderItemInline(admin.StackedInline):
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 0 # تعداد ستونهای اضافه ای که اونور برامون به صورت پیش فرض میذاره
    min_num = 1 # یعنی حداقل باید یه دونه بذاریم. منطقی هم هست. چون سفارش نمیشه بدون آیتم باشه که
    # max_num = 10 # اگه بخوایم مثلا تو یه سفارش بیشتر از ۱۰ نوع آیتم نتونه سفارش بده


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'customer', 'datetime_created', 'num_of_items']
    list_display_links = ['id', 'customer', 'datetime_created', 'num_of_items']
    list_editable = ['status']
    list_per_page = 20
    ordering = ['-datetime_created']
    inlines = [OrderItemInline]

    # برای پریفچ ریلیتد، مثل سلکت ریلیتد متغیر تعریف نکردن. اما میتونیم کوئری که برای درخواست میزنه
    # رو تغییر بدیم که با دستورات بهتری از دیتابیس سوال بپرسیم. برای همون پروداکت اول هم که از
    # لیست سلکت ریلیتد استفاده کرده بودیم از همین مدل استفاده کرد با سلکت ریلیتدی که خودم نوشتم
    # به درستی کار میکرد. اما خب به هر حال تعریف متغیر رو هم بلد باشیم خوبه و بد نیست
    # هر دو مدل رو الان بلدم 😊
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items').annotate(items_count=Count('items'))

    @admin.display(ordering='items_count')
    def num_of_items(self, order: Order):
        # return order.items.count()
        return order.items_count # وقتی خودمون با انوتیت آیتم کَونت رو درست کردیم، دیگه میتونیم مستقیما هم از خود متغیرش استفاده کنیم اینجا و لازم نیست متد کَونت رو رو منیجر آیتمز صدا کنیم تا تعداد رو به ما بده


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status', 'name', 'body']
    list_display_links = ['id', 'product']
    list_editable = ['status']
    list_per_page = 25
    search_fields = ['product__first_name']
    autocomplete_fields = ['product'] # دقت کنم که این جا اضافه کنیم همین طوری ارور میده. میگه که
    # باید به پروداکت سرچ فیلد اضافه کنی تا بتونم این رو درست کنم. اونجا که تو کلاس پروداکت ادمین
    # بهش سرچ فیلد بدیم این درست میشه فقط این که اینجا قرار نیست کوئری عالی بزنیم
    # و بین چیزهای زیاد بیایم حرفه ای سرچ کنیم. و وقتی که من ۲ تا گذاشتم یا icontains با ۲ تا گذاشتم
    # جواب نمیداد بهم. اما وقتی یه دونه اش کردم درست شد و کار میکرد به درستی


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'full_name', 'email', 'phone_number']
    list_display_links = ['first_name', 'last_name', 'full_name', 'email', 'phone_number']
    list_per_page = 50
    ordering = ['last_name', 'first_name']
    search_fields = ['last_name__istartswith', 'first_name__istartswith']

    @admin.display(ordering='first_name', description='نام کامل') # اگه بخوایم اسم ستونی که گذاشته رو عوض کنیم از دیکریپشن استفاده میکنیم.
    def full_name(self, customer: Customer):
        return f"{customer.first_name} {customer.last_name}"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    autocomplete_fields = ['product', ]


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ['id', 'product', 'quantity']
    extra = 0
    min_num = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_display_links = ['id', 'created_at']
    inlines = [CartItemInline]


admin.site.register(Category)
