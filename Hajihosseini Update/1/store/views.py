from django.shortcuts import render
from django.db import transaction

from .models import Product, Address, Comment, Cart, CartItem, Category, Customer, Discount, OrderItem, Order


def printype(x):
    print(x, type(x))


def typerint(x):
    print(type(x), x)

# مربوط به ترنسکشن اتمیک از فصل کوئری های پیشرفته (فصل ۵ آپدیت) سر تمرینش که رسیدم توضیح هست
# @transaction.atomic()
def show_data(request):
    context = {
        'alaki': 12345
    }

    # query_set = Product.objects.all() # متد آل، خروجی به ما کوئری ست میده تا وقتی تبدلیش به لیست نکنیم یا اسلایسش نکنیم یا استفاده نکنیم، به دیتابیس هیت نمیکنه
    # printype(query_set)

    # product = Product.objects.get(id=700) # متد گیت، یک آبجکت از اون کلاس رو به ما میده دیگه کوئری ست نیست. آبجکت هست. حتی اگه ازش استفاده هم نکنیم به دیتابیس هیت میزنه. چون یه آبجکت به ما میده و سریع هست، خیلی طول نمیکشه اغلب 
    # product = Product.objects.get(name='Scientist How Then') # لازم نیست حتما گت رو روی آی دی صدا کنیم. اما حواسمون باشه که یه چیز یونیک باشه. اگه یونیک نباشه و ۲ یا چند تا ازش موجو باشه، به ما ارور میده. اگه پیدا هم نکنه باز ارور میده. تنها در صورتی جواب میده که یه دونه پیدا کنه. به خاطر همین معمولا با آی دی یا یه چیز یونیک به کار میره. با این حال باز هم ممکنه پیدا نکنه و ارور بده که برای رفعش بهتره از گت آبجکت ار ۴۰۴ استفاده کنیم که ارور نده به ما.
    # printype(product.id)
    # printype(product.name)
    # printype(product.unit_price)

    # query_set = Product.objects.filter(id=700) # فیلتر کوئری ست به ما تحویل میده. باز هم لیزی هست. خوبیش اینه که بیشتر از یه دونه پیدا کنه ارور نمیده. هیچی هم پیدا نکنه ارور نمیده.
    # product = query_set[0] # روش پایتونی که خودمون اولی رو بگیریم بعد از فیلتر
    # product = query_set.first() # روش اس کیو الی که اولی رو بگیریم. در واقع تو دستور اس کیو الی که میفرسته ORDER BY ASC LIMIT 1 رو ته دستور اعمال میکنه 
    # product = query_set.last() # روش اس کیو الی که آخری رو بگیریم. در واقع تو دستور اس کیو الی که میفرسته ORDER BY DESC LIMIT 1 رو ته دستور اعمال میکنه 
    # product = query_set[-1] # ارور میده. چون لیست یا تاپل نیست. بلکه یک کوئری ست جنگو هست و اندیس منفی براش تعریف نکردند.
    # length = len(query_set) # روش پایتونی خودم که آخرین آیتم رو بگیریم بعد از فیلتر.
    # product = query_set[length-1]
    # print(product.id)
    # print(product.name)
    # print(product.unit_price)

    # خلاسه هر ۴ روش ممکنه ارور بدن. خودمون باید بررسی کنیم ببینیم که فیلتر به ما جواب
    # داده یا نه. اما یه متد هم برای کوئری ست ها نوشتن که میتونیم ازش استفاده کنیم
    # به ما جواب ترو و فالس میده و میتونیم از اون استفاده کنیم.
    # با این حال دقت کنم که خودش یک کوئری جداگانه میفرسته که ببینه چنین چیزی وجود
    # داره یا نه. یعنی تو این مثال که یه کوئری و یک هیت به دیتابیس اضافه میشد وقتی
    # متد دات اگزیستس رو استفاده کردم.
    # query_set = Product.objects.filter(id=1700)
    # if query_set.exists():
    #     product = query_set.first() # روش اس کیو الی که اولی رو بگیریم. در واقع تو دستور اس کیو الی که میفرسته ORDER BY ASC LIMIT 1 رو ته دستور اعمال میکنه 
    # else:
    #     product = "این محصول وجود ندارد"
    # print(product)
    #############################################################################
    #############################################################################
    ############################       Lookups       ############################
    #############################################################################
    #############################################################################
    # query_set = Product.objects.filter(inventory=5) # WHERE inventory = 5
    # query_set = Product.objects.filter(inventory__lt=5) # WHERE inventory < 5
    # query_set = Product.objects.filter(inventory__lte=5) # WHERE inventory <= 5
    # query_set = Product.objects.filter(inventory__gt=95) # WHERE inventory > 5
    # query_set = Product.objects.filter(inventory__gte=95) # WHERE inventory >= 5
    # query_set = Product.objects.filter(inventory__in=[5, 13, 40]) # WHERE inventory in (5, 13, 40)
    # query_set = Product.objects.filter(inventory__in=(5, 13, 40)) # WHERE inventory in (5, 13, 40)
    # query_set = Product.objects.filter(name__contains='Knowledge') # WHERE name BINARY '%Knowledge%'
    # query_set = Product.objects.filter(name__icontains='Knowledge') # WHERE name '%Knowledge%'
    # query_set = Customer.objects.filter(birth_date__isnull=True) # WHERE birth_date IS NULL
    # query_set = Customer.objects.filter(birth_date__isnull=False) # WHERE birth_date IS NOT NULL
    # query_set = Product.objects.filter(category=2) # WHERE category_id=2 خودش چون فارین کی هست، آی دی گذاشته
    # query_set = Product.objects.filter(category_id=2) # WHERE category_id=2 خودمون نوشتیم :دی
    # query_set = Product.objects.filter(category__id=2) # WHERE category_id=2 خودش تبدیل کرده بود به این :دی
    # query_set = Product.objects.filter(category__title__icontains="Knowledge") # product INNER JOIN ON category WHERE category.title LIKE '%Knowledge%'
    # print(len(query_set))
    # query_set = Product.objects.filter(category__title__icontains="Knowledge") # SELECT chizaye table e avvali FROM product INNER JOIN ON category WHERE category.title LIKE '%Knowledge%'
    # ولی وقتی بخوایم چیزی از توش در بیاریم، کند میشه و هیت الکی میزنه به دیتابیس که جلوتر راجع به سلکت ریلیتد صحبت میشه. اما فعلا بحث لوکاپ ها هست و این دستور پایین کافیه که حالا که تو دستورش داره جوین میکنه، پس موقع سلکت میگه اونا رو هم که تو تیبل دوم هستند بگیر.
    # query_set = Product.objects.filter(category__title__icontains="Knowledge").select_related('category') # SELECT chizaye table e avval va dovvom FROM product INNER JOIN ON category WHERE category.title LIKE '%Knowledge%'
    # for product in query_set:
    #     print(product.category.title)
    # query_set = Product.objects.filter(datetime_created__year=2019) # WHERE `store_product`.`datetime_created` BETWEEN '2019-01-01 00:00:00' AND '2019-12-31 23:59:59.999999'
    # print(len(query_set))
    
    # ترکیبی
    # query_set = Product.objects.filter(name__icontains='site', inventory__gt=5, datetime_created__month=6) # WHERE (EXTRACT(MONTH FROM `store_product`.`datetime_created`) = 6 AND `store_product`.`inventory` > 5 AND `store_product`.`name` LIKE '%site%')
    # print(len(query_set))
    # لینک فیلد لوکاپ های کوئری ست ها  django queryset field lookups سرچ کردم
    # https://docs.djangoproject.com/en/5.0/ref/models/querysets/

    #############################################################################
    ############################# تمرین های سری اول فصل ORM & queries. در حال حاضر فایل ۳۳۲ 
    #############################################################################
    # #1 تمام اردرآیتم هایی که محصول ۱ توشون هست.
    # query_set = OrderItem.objects.filter(product=1) # روش ۱ که استفاده کرده بودم :)
    # query_set = OrderItem.objects.filter(product__id=1) # روش ۲ که موقع توضیح گفت
    # query_set = OrderItem.objects.filter(product_id=1) # روش ۳ که موقع توضیح گفت
    # جوابش برای ۱، ۰ تا بود. بعد ۲ رو زدم اونم صفر بود. خواستم محدوده بدم واین شکلی زدم
    # query_set = OrderItem.objects.filter(product__range=(1,50)) # ارور میده Unsupported lookup 'range' for ForeignKey or join on the field not permitted.
    # اما ارور میداد و مینوشت که از لوکاپ رنج نمیشه برای فارین کی استفاده کرد.
    # دیگه زیاد توضیح نمیدم. روش های زیر رو میشه انجام داد.
    # query_set = OrderItem.objects.filter(product__in=(1,2,3,4,5, ,50)) # که به درد نمیخوره
    # query_set = OrderItem.objects.filter(product__in=range(1, 50)) # که از لوکاپ in در ORM جنگو استفاده میکنیم و تابع رنج پایتون. و در اس کیو ال هم از اپراتور IN استفاده میکنه.
    # query_set = OrderItem.objects.filter(product__id__range=(1, 50)) # که از لوکاپ رنج ORM استفاده میکنیم و در اس کیو ال از دستور BETWEEN استفاده میکنه و این بار کار هم میکنه.
    # query_set = OrderItem.objects.filter(product_id__range=(1, 50)) # دقت کنم که این هم مثل همون ورژن من ارور میده.
    # در واقع تو حل این تمرین، روش ۱ که خودم انجام داده بودم و روش ۳، تو دیتابیس
    # سراغ تیبل دوم نمیرن و از همون اطلاعات تیبل اول استفاده میکنن. به خاطر همین هست
    # که لوکاپ رنج روشون کار نمیکنه. اما روش دوم که با دو تا ــ هست، سراغ تیبل دوم
    # هم میره و وقتی رفت اونجا، دیگه آی دی اون تیبل رو داره و میتونه رنج رو روش
    # صدا بکنه و ازش استفاده کنه. یه نتیجه گیری کوتاه هم بگم
    # لوکاپ این تو دستورات تبدیل میشه به اپراتون IN در زبان sql
    # لوکاپ رنج تو دستورات تبدیل میشه به اپراتور BETWEEN در زبان sql
    # print(len(query_set))

    # #2 تمام محصولاتی که ازشون ۵ تا مونده
    # query_set = Product.objects.filter(inventory=5)
    # print(len(query_set))
    
    # #3 تمام محصولاتی که توشون کلمه سایت باشه (کیس اینسنسیتیو) و بیشتر از ۳ تا ازشون مونده
    # query_set = Product.objects.filter(name__icontains='site', inventory__gt=3)
    # print(len(query_set))
    
    # #4 تمام محصولاتی که توشون کلمه سایت باشه (کیس اینسنسیتیو) و بیشتر از ۳ تا ازشون مونده و کمتر از ۱۰ تا
    # query_set = Product.objects.filter(name__icontains='site', inventory__gt=3, inventory__lt=10) # روش اول
    # query_set = Product.objects.filter(name__icontains='site', inventory__range=(4, 9)) # روش دوم
    # دقت کنم که لوکاپ رنج چون از BETWEEN استفاده میکنه، خود اون ۲ عددرو هم شامل میشه.
    # پس برای کوئری خواسته شده حداقل رو یکی زیاد کردم و حداکثر رو یکی کم کردم
    # نکته مهم آخر این که تو BETWEEN حتما عدد اول باید کوچیکتر باشه و دومی بزرگتر
    # یعنی اگه جای ۴ و ۹ رو عوض کنم بهم ارور نمیده. اما جواب هم نمیده. حالا شاید تو
    # این مثال جواب هر دو تا ۰ آیتم باشه. اما اگه تو رنج عدد اول بزرگتر و عدد دوم
    # کوچیکتر باشه، همیشه ۰ جواب به ما میده. چون از نظر منطقی اون حالت ممکن نیست.
    # print(len(query_set))
    
    # #5 تمام سفارش های پرداخت نشده
    # query_set = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)
    # print(len(query_set))
    # #5.5 تمام سفارش هایی که پرداخت نشده نیستند. موقع حل اضافه کرد
    # query_set = Order.objects.filter(status__in=[Order.ORDER_STATUS_PAID, Order.ORDER_STATUS_CANCELED]) # روش noobiew :D
    # query_set = Order.objects.exclude(status=Order.ORDER_STATUS_UNPAID) # روش صحیح و اصولی و سریعتر که تو اس کیو ال هم از اپراتور NOT استفاده میکنه. روش نوبی اول که استفاده کردم از دستور این با چند آیتم استفاده میکرد
    # print(len(query_set))
    
    #6 تمام اردر آیتم هایی که برای سفارش اول هستند.
    # همون داستان های اولی. هر ۳ تاش کار میکنه.
    # query_set = OrderItem.objects.filter(order=1)
    # query_set = OrderItem.objects.filter(order_id=1)
    # query_set = OrderItem.objects.filter(order__id=1)
    # print(len(query_set))
    #6.5 موقع حل اضافه کرد. تمام اردرآیتم هایی که برای اردر ۱ هستند و بیشتر از ۱۰ تا خرید نشدن
    # query_set = OrderItem.objects.filter(order=1).exclude(quantity__gt=10) # روش ۱
    # query_set = OrderItem.objects.filter(order=1, quantity__lte=10) # روش ۲
    # print(len(query_set))


    # #7 تمام محصولات کمتر از ۱۰ دلار
    # query_set = Product.objects.filter(unit_price__lt=10)
    # print(len(query_set))

    #8 تمام اردرآیتم هایی که توسط مشتری های به اسم جان خریداری شدند (تو اسمشون کلمه جان به کار رفته)
    # query_set = OrderItem.objects.filter(order__customer__first_name__icontains='john').select_related('order__customer') # این سلکت ریلیتدی که از دو لایه بعدتر نوشتم، باعث میشه خودش هم تمام چیزهای اردر رو بگیره هم تمام چیزهای کاستومر. یعنی لازم نیست هم رو order سلکت ریلیتد بزنم هم رو order__customer. فقط order__customer رو که بزنم کافیه.
    # for order_item in query_set:
    #     print(order_item.order.customer.first_name)
    #8.5 احتمالا موقع حل حواسش پرت شده بود. تمام اردرها رو گرفت. در واقع اونی که من حل کردم سخت تر بود. تو سوال ۸ تمام اردر آیتم ها رو با اون ویژگی گرفتیم. اما تو حل تمام اردر ها با اون ویژگی رو گرفت که الان این رو به دو روش حل میکنم.
    # روش خودش
    # query_set_john = Customer.objects.filter(first_name__icontains='john')
    # query_set = Order.objects.filter(customer__in=query_set_john).select_related('customer') # البته هنوز سلکت ریلیتد رو درس نداده و خودم اینجا اضافه کردم برای سرعت بیشتر.
    # for order in query_set:
    #     print(order.customer.first_name)
    # روش من
    # query_set = Order.objects.filter(customer__first_name__icontains='john').select_related('customer') # البته هنوز سلکت ریلیتد رو درس نداده و خودم اینجا اضافه کردم برای سرعت بیشتر.
    # for order in query_set:
    #     print(order.customer.first_name)
    #############################################################################
    ############################# پایان تمرین های سری اول فصل ORM & queries
    #############################################################################
    #############################################################################
    #############################################################################
    ##########################       end Lookups       ##########################
    #############################################################################
    #############################################################################




    #############################################################################
    #############################################################################
    #######################       Advanced Queries       ########################
    #############################################################################
    #############################################################################
    # Q object
    # اطلاعات مشتری هایی رو به ما بده که تو اسمشون john به کار رفته. یا تو فامیلیشون یا تو ایمیلشون
    # روش نوبی اول :D
    # query_set = Customer.objects.filter(first_name__icontains='john')
    # for customer in query_set:
    #     print(customer.first_name, customer.last_name, customer.email)
    # query_set = Customer.objects.filter(last_name__icontains='john')
    # for customer in query_set:
    #     print(customer.first_name, customer.last_name, customer.email)
    # query_set = Customer.objects.filter(email__icontains='john')
    # for customer in query_set:
    #     print(customer.first_name, customer.last_name, customer.email)
    # که اگه نخوایم پرینت کنیم، باید یه لیست از مشتریها درست کنیم و اینا رو توشون اپند کنیم.
    # بریم روش خفن و حرفه ای
    # from django.db.models import Q
    # AND رو خود متد فیلتر با ویرگول میفهمه. اما OR رو نمیفهمه. میتونیم از کیو آبجکت این شکلی استفاده کنیم.
    # query_set = Customer.objects.filter(Q(first_name__icontains='john') | Q(last_name__icontains='john') | Q(email__icontains='john'))
    # for customer in query_set:
    #     print(customer.first_name, customer.last_name, customer.email)
    # معمولا از & استفاده نمیشه. اما اگه لازم بشه، به جای پایپ همین علامت امپرسند رو میذاریم.
    # چرا ممکنه لازم بشه، اگه یه کوئری بخوایم بنویسیم که توش چند تا اند و اور و نات به کار
    # رفته، میتونیم برای همه شون بنویسیم که خوانایی کد راحت تر باشه
    # مثلا کسایی که تو اسم یا فامیلشون so به کار رفته. و تو ایمیلشون هم کلمه
    # example به کار رفته رو میشه به روش های زیر نوشت. تصمیم انتخاب این که از کودوم استفاده کنم با خودم.
    # query_set = Customer.objects.filter(Q(first_name__icontains='so') | Q(last_name__icontains='so') & Q(email__icontains='example'))
    # query_set = Customer.objects.filter(Q(first_name__icontains='so') | Q(last_name__icontains='so'), Q(email__icontains='example'))
    # query_set = Customer.objects.filter(Q(first_name__icontains='so') | Q(last_name__icontains='so'), email__icontains='example')
    # query_set = Customer.objects.filter((Q(first_name__icontains='so') | Q(last_name__icontains='so')) & Q(email__icontains='example'))
    # query_set = Customer.objects.filter((Q(first_name__icontains='so') | Q(last_name__icontains='so')), Q(email__icontains='example'))
    # query_set = Customer.objects.filter((Q(first_name__icontains='so') | Q(last_name__icontains='so')), email__icontains='example')
    # برای نات کردن هم از تیلدا استفاده میشه. یه مثلا ساده میزنم. میدونم که میشه راحت
    # برعکسش کرد و بدون Q هم نوشت. اما صرفا مثال هست.
    # محصولاتی که بیشتر از ۵ تا موجودیشون نیست.
    # query_set = Product.objects.filter(~Q(inventory__gt=5))
    # print(len(query_set))

    # F object احتمالا فیلد آبجکت باشه با توجه به توضیحات. به هر حال
    # اگه بخوایم مثلا مشتری هایی رو پیدا کنیم که اسم و فامیلشون یکی هست، با چیزایی که تا
    # حالا تو جنگو یاد گرفتیم نمیشه. دستور دیتابیسش ساده هست. اما شیوه نمایشش رو تا حال
    # تو جنگو یاد نگرفتیم. یا مثلا محصولاتی که قیمتشون با تعداد باقیمونده تو انبار یکی
    # هست. اینا صرفا مثال هست. شاید کوئری شون منطقی نباشه. اما صرفا مثاله.
    # به هر حال الان میخوام افرادی رو پیدا کنم که اسمشون با فامیلشون یکی هست.
    # برای این از F استفاده میکنیم. به این صورت
    # from django.db.models import F
    # query_set = Customer.objects.filter(first_name=last_name) این شکلی نمیشه استفاده کرد و ارور میده
    # query_set = Customer.objects.filter(first_name=F('last_name'))
    # print(len(query_set))
    # که کسی رو پیدا نکرد اما دستورش این بود
    # WHERE `store_customer`.`first_name` = (`store_customer`.`last_name`)
    # که از نظر اس کیو ال دستور ساده ای هست. حالا برای این که جواب داشته باشه،
    # محصولاتی که تعداد باقیمانده شون از قیمتشون بیشتر باشه. شاید به کاری نیاد ولی
    # خب یه کوئری هست که احتمال زاید جواب داره.
    # query_set = Product.objects.filter(inventory__gt=F('unit_price')) # WHERE `store_product`.`inventory` > (`store_product`.`unit_price`)
    # print(len(query_set))

    # indexing
    # البته منظورش ایندکسینگ پایتون هست فکر کنم. نه ایندکسی که اس کیو ال استفاده میکن
    # query_set = Product.objects.all()[550:620] # SELECT * FROM `store_product` LIMIT 70 OFFSET 550
    # print(len(query_set))

    # order_by and reverse
    # query_set = Product.objects.filter(inventory__lt=3).order_by('unit_price') # ... ORDER BY `store_product`.`unit_price` ASC
    # query_set = Product.objects.filter(inventory__lt=3).order_by('-unit_price') # ... ORDER BY `store_product`.`unit_price` DESC
    # query_set = Product.objects.filter(inventory__lt=3).order_by('unit_price').reverse() # ... ORDER BY `store_product`.`unit_price` DESC
    # for product in query_set:
    #     print(product.name, product.inventory, product.unit_price)

    # earliest latest
    # query_set = Product.objects.filter(inventory__lt=5) # این چیکار میکنه؟
    # اونایی که کمتر از ۵ تا موندن رو به ما میده. حالا اگه بخوایم بین اینها گرونترین
    # رو پیدا کنیم میتونیم این کار رو بکنیم.
    # query_set = Product.objects.filter(inventory__lt=5).order_by('unit_price').last()
    # یا
    # query_set = Product.objects.filter(inventory__lt=5).order_by('-unit_price').first()
    # یا
    # query_set = Product.objects.filter(inventory__lt=5).latest('unit_price')
    # یا
    # query_set = Product.objects.filter(inventory__lt=5).earliest('-unit_price')
    # هر چهار حالتی که نوشتم خروجی اس کیو الشون میشه این دستور
    # WHERE `store_product`.`inventory` < 5 ORDER BY `store_product`.`unit_price` DESC LIMIT 1
    # حتی میشه به روش های دیگه هم انجام داد. مثلا همون اردر بای رو بذاریم و بعد با اندیس
    # ۰ پایتون اولی رو پیدا کنیم. اما اندیس منفی ۱ نمیشه گذاشت برای آخری و باید
    # طولش رو پیدا کنیم و منهای ۱ ش بکنیم که خب چه کاری هست الکی پیچیده کنیم
    # به جای اردر بای کردن و بعد گرفتن اولی یا آخری، میتونیم مستقیما بهش بگیم که اولین
    # یا آخرین آیتم از یکی چیزی رو میخوایم که حالا اون چیز رو مستقیما داخل پرانتز به عنوان
    # ورودی میتونیم بهش بدیم. مثل دستورهای سوم و چهارم که راحت تر هستند.
    # print(query_set)
    # به عنوان آخرین مثال این موضوع هم الان میخوام گرونترین محصول سایت رو بگیرم
    # query_set = Product.objects.latest('unit_price')
    # یا
    # query_set = Product.objects.earliest('-unit_price')
    # print(query_set)

    # values برای اینه که ستون های خاصی رو از تیبل بگیریم.
    # نکته ای که داره اینه که دیگه آبجکت رو به ما تحویل نمیده. توی پایتون تبدیلش میکنه
    # به یه دیکشنری که اون کلید ها رو داره. به خاطر همینه که تو حلقه فور پایین،
    # مجبور شدم از تابع گت دیکشنری استفاده کنم که بتونم نشونش بدم. چون هر item
    # یه دیکشنری بود با کلید های نام و اینونتوری. نه این که هر آیتم یه نمونه از کلاس
    # Product باشه
    # query_set = Product.objects.all().order_by('-inventory').values('name', 'inventory')
    # for item in query_set:
    #     # print(item.name, item.inventory) # ارور میده
    #     print(item.get('name'), item.get('inventory'))
    # در واقع شبیه همون کاری که خودم تو پروژه قائن کرده بودم. اگه لازم نباشه که
    # جایی همه چیز رو بگیریم، بعضی هاش رو از دیتابیس میگیریم و تو یه دیکشنری ذخیره
    # میکنیم و تو برنامه از اون دیکشنریه استفاده میکنیم. در مورد only یه کم جلوتر
    # صحبت میکنیم. اما یه متد دیگه هم هست به اسم values_list که برای توضیحش دوباره
    # همین مثالی که زدم رو تکرار میکنم.
    
    # values_list تکرار دوباره برای معرفی متد
    # query_set = Product.objects.all().order_by('-inventory').values('name', 'inventory')
    # for item in query_set:
    #     print(item)
    # این حلقه هر بار یه دیکشنری با همون کلید ها و مقدارها بهمون میده. در واقع
    # query_set = Product.objects.all().order_by('-inventory').values('name', 'inventory')
    # print(list(query_set))
    # در واقع اگه به این دقت کنم، میبینم که هر عضو این لیست یه دیکشنری هست که داخلش
    # کلیدهای نام و اینونتوری رو داریم. ولی خب ۱۰۰۰ بار هی مینویسه نام فلان هست
    # اینونتوری هم فلان مقدار هست. دفعه بعد دوباره میگه نام فلان هست. مقدار اینونتوری
    # هم فلان قدر هست. یه بار گفتی بسه دیگه. :D
    # اگه یه وقت بخوایم که دیگه هر بار به ما نده
    # و خودمون فقط از مقادیرش استفاده کنیم، میتونیم از متد values_list استفاده کنیم.
    # query_set = Product.objects.all().order_by('-inventory').values_list('name', 'inventory')
    # print(list(query_set))
    # این شکلی دیگه فقط مقادیر رو داریم. به جاش موقع استفاده هم دیگه دیکشنری نیست
    # و با اندیس باید پیداشون کنیم یعنی
    # query_set = Product.objects.all().order_by('-inventory').values_list('name', 'inventory')
    # for item in query_set:
    #     # print(item.get('name'), item.get('inventory')) # ارور میده. چون دیکشنری نیست و تاپله
    #     print(item[0], item[1])
    # این شد از تفاوت متدهای values و values_list

    # distinct حذف آیتم های تکراری از نتیجه
    # با یه مثال توضیح بدم.
    # query_set = OrderItem.objects.all()
    # print(len(query_set))
    # این کوئری، لیست تمام اردرآیتم ها رو به ما میده. حالا ما از کوئری بعدی استفاده میکنیم
    # query_set = OrderItem.objects.all().values('product')
    # print(len(query_set))
    # این کوئری، لیست تمام اردرآیتم ها رو به ما میده. منتهی فقط این که به چه محصولی وصل بودن
    # در واقع آی دی تمام محصولاتی رو به ما میده که حداقل تو یه اردرآیتم اومدن.
    # خب حالا فرض کنیم ما میخوایم لیست محصولاتی رو داشته باشیم که حداقل یه سفارش داشتن
    # اما تو این لیست، کلی آیتم تکراری داریم. یعنی چیزی که توسط ۲۰ نفر هم خریداری شده،
    # ۲۰ بار تو این نتیجه اومده. اما ما فقط میخوایم بدونیم که محصولی خریداری شده یا نه.
    # اینجاست که از دیستینکت استفاده میکنیم.
    # query_set = OrderItem.objects.all().values('product').distinct()
    # print(len(query_set))
    # تو دیتابیسی که داشتم با اون اطلاعات فیک، قبلی ۱۶۷ مورد بهم میداد. و محصول ۹۹۳
    # ۴ بار تکرار شده بود. اما بعد از دیستینک تعدادش رسید به ۱۵۰ و محصول ۹۹۳ فقط
    # یک بار تو نتیجه بود. همین طور در مورد آیتم های دیگه. یعنی از ۱۶۷ رسیدیم به ۱۵۰
    # و محصولاتی که چند بار خریداری شده بودند، با دیستینکت به ۱ بار کاهش یافتند.
    # در واقع جلوتر که دارم تمرین رو حل میکنم، تو روش مزخرف اولیه خودم اومدم از
    # مجموعه های پایتون استفاده کردم. اگه از لیست استفاده میکردم، ۱۶۷ تا آیتم
    # بهم میداد. اما وقتی مجموعه گذاشتم، تکراری ها دیگه اضافه نشدند و همون ۱۵۰
    # رو بهم نشون داد. حالا به تمرین رسیدم دوباره توضیح میدم.

    # تمرین: لیست محصولاتی که حداقل تو یه اردر آیتم وجود داشتند
    # روش مزخرف اول که بسیار کند هست. هم از نظر دیتابیس و هم از نظر پایتون
    # query_set_order_items = OrderItem.objects.all().values('product')
    # products=set()
    # for item in query_set_order_items:
    #     product = Product.objects.get(id=item.get('product'))
    #     products.add(product)
    # for product in products:
    #     print(product.name, product.unit_price)
    # print(len(products))
    # روش مزخرف دوم که بسیار کند هست. هم از نظر دیتابیس و هم از نظر پایتون و تفاوت چندانی نداره
    # query_set_order_items = OrderItem.objects.all()
    # products=set()
    # for item in query_set_order_items:
    #     products.add(item.product)
    # for product in products:
    #     print(product.name, product.unit_price)
    # print(len(products))
    # روش سوم که خودش انجام داد
    # query_set_order_items = OrderItem.objects.values('product').distinct()
    # query_set = Product.objects.filter(id__in=query_set_order_items)
    # print(len(query_set))
    # روش چهارم من که از ریلیتد نیم استفاده کردم و مستقیما کوئری رو به جای اردرآیتم،
    # رو پروداکت زدم جواب درست بود. اما بر اساس آی دی مرتب نمیکرد.
    # این شد که خودم مرتب هم کردم.
    # query_set = Product.objects.filter(order_items__quantity__gt=0).distinct().order_by('id')
    # print(len(query_set))
    # دستور اس کیو ال مربوط به کد حاجی حسینی # SELECT * FROM `store_product` WHERE `store_product`.`id` IN (SELECT DISTINCT U0.`product_id`  FROM `store_orderitem` U0)
    # دستور اس کیو ال مربوط به کد آخر من # SELECT DISTINCT * FROM `store_product` INNER JOIN `store_orderitem` ON (`store_product`.`id` = `store_orderitem`.`product_id`) WHERE `store_orderitem`.`quantity` > 0 ORDER BY `store_product`.`id` ASC
    # آخرین نکته مهم این که وقتی تو دستور خودم دیستینکت رو حذف میکردم، جوابی که بهم میداد
    # ۱۶۷ تا میشد. پس حتما باید تو دستوری که من نوشتم دیستینکت رو بذاریم تا به درستی جواب
    # بده. اما تو دستور حاجی حسینی که دیستینکت رو برداشتم، باز هم ۱۵۰ تا میشد.
    # یعنی بدون دیستینکت هم درست کار میکرد. تو توضیحاتش هم گفته بود که میشه تو این مثال
    # نذاشت. از نظر منطقی این دو تا دستور اس کیو ال رو بررسی کنم مشخص میشه که چرا دستور
    # حاجی حسینی دیستینکت رو لازم نداره. در واقع تو سلکت داخلی ۱۶۷ تا جواب به ما میده
    # اما تو سلکت اولی، میگه که اگه تو این ۱۶۷ تا بود که از این ۱۶۷ تا، ۱۷ تاش تکراری
    # هستند. پس اگه تکراری ها رو حذف بکنیم یا نکنیم، سلکت بیرونی همون ۱۵۰ تا رو به ما
    # تحویل میده. خلاصه این که دستور حاجی حسینی خفن تره :)

    # only 💀
    # قبلا راجع به values صحبت کردیم. متد ولیوز، کاری که میکنه یه دیکشنری از فیلدهایی
    # که گفتیم برای ما درست میکنه و به ما میده. و ارسال میکنیم، یه دیکشنری با مقادیر
    # مشخص ارسال میکنه و نمیدونه که بخشی از یک آبجکت بودن. اما متد only
    # نحوه نوشتنش مثل همون ولیوز هست. با این تفاوت که دیگه یه دیکشنری درست نمیکنه.
    # بلکه یه نمونه واقعی از اون کلاس رو پاس میده برای اچ تی ام ال. یعنی یک دیکشنری نیست
    # و آبجکت واقعی هست. اما ما چون بهش گفتیم فقط این فیلدها رو بگیر، خب اون هم از تیبل
    # بقیه رو نمیگیره. 💀 قسمت خطرناکش اینجاست که اگه ما مثلا بگیم نام و آی دی همه محصولات
    # رو بگیر و بفرست به فرانت، اون ور تا وقتی که با نام و آی دی کار داشته باشیم
    # و مثلا روشون حلقه بزنیم مشکلی نیست. اما اگه مثلا بگیم تعداد اینونتوری هر محصول رو
    # هم بگیر، وقتی میبینه که تو محصول نیست، چون میدونه که محصول هست و تو تیبل یه مقداری
    # داشته، هیت میزنه به دیتابیس و وقتی یه حلقه نوشته باشیم، باز هم هیت میزنه و غیره
    # که این طوری مثلا ۱۰۰۰ بار هیت میزنه به دیتابیس و سرعت رو خیلی کم میکنه. نه این که
    # استفاده ازش بد هست. اما باید با دقت خیلی زیادی استفاده بشه. اگه ولیوز استفاده کنیم
    # وقتی تو فرانت بهش میگیم تعداد اینونتوری رو نشون بده، اون خبر نداره که ما محصولات
    # رو براش فرستادیم و فقط فکر میکنه دیکشنری هست. توش دنبال اینونتوری میگرده و برای
    # هر محصول که وجود نداره، چیزی نمینویسه. اما خب کند هم نمیشه. 
    # یه نمونه محض این که داشته باشم.
    # query_set = Product.objects.only('id', 'unit_price')
    # for product in query_set:
    #     print(product.id, product.unit_price) # Ok
    #     print(product.id, product.unit_price, product.inventory) # 💀 خانمان سوز 😁
    # query_set = Product.objects.only('id', 'unit_price', 'inventory')
    # for product in query_set:
    #     print(product.id, product.unit_price, product.inventory) # دوباره اوکی.
    # پس اگه لازم شد از only استفاده کنم، دقت کنم

    # defer 💀
    # دیفر هم دقیقا برعکس only هست. خود آبجکت رو به ما میده. منتهی چیزهایی که نمیخوایم
    # رو داخل متد دیفر مینویسیم. مثلا
    # query_set = Product.objects.defer('name', 'category', 'slug', 'description', 'datetime_created', 'datetime_modified', 'discounts')
    # for product in query_set:
    #     print(product.id, product.unit_price, product.inventory) # OK
    #     print(product.id, product.unit_price, product.inventory, product.name) # 💀 خانمان سوز 😁
    
    # select_related 💙💚💖
    # گرفتن تمام اطلاعات تمام اردرآیتم ها
    # query_set = OrderItem.objects.all()
    # for order_item in query_set:
    #     print(order_item.id, order_item.quantity, order_item.unit_price) # Ok.
        # print(order_item.order) # خانمان سوز ۱ 😁
        # print(order_item.product) # خانمان سوز ۲ 😁
        # print(order_item.order, order_item.product) # این که دیگه هیچی. دنیا رو نابود میکنه
    # چون توضیحش رو بلدم و خیلی شبیه آنلی هست، فقط راه حل رو مینویسم که با استفاده از
    # سلکت ریلیتد، موقعی که رفت سراغ تیبل بهش میگیم که اینر جوین بزنه بقیه اطلاعات
    # رو هم بگیره دیگه الکی بعدا برنگرده سراغ دیتابیس. یعنی این شکلی
    # query_set = OrderItem.objects.all().select_related('order', 'product')
    # for order_item in query_set:
    #     print(order_item.order, order_item.product, order_item.product.inventory) # OK
    # اسم اون فیلدی که فارین کی هست رو داخل متد سلکد ریلیتد مینویسیم که اون تیبل رو هم
    # بگیره. حالا میتونیم داخل اونها رو هم بخوونیم. مثل همین اینونتوری که تو پرینت نوشتم.
    # تمرین: لیست تمامی اردرآیتم ها با محصولاتشون و عنوانشون و تعدادشون
    # query_set = OrderItem.objects.all().select_related('product')
    # for order_item in query_set:
    #     print(order_item.product, order_item.product.name, order_item.product.inventory)

    # prefetch_related 🧡💛🤍
    # برای تمام محصولات، میخوایم اطلاعات اردرآیتم هاشون رو بنویسیم.
    # دقت کنم که سلکت ریلیتد کرده بودیم به محصولات با نام order_items
    # query_set = Product.objects.all()
    # for product in query_set:
    #     for order_item in product.order_items.all():
    #         print(order_item) # 💀 خانمان سوز
    # برای حلش از prefetch_related استفاده میکنیم.
    # query_set = Product.objects.all().prefetch_related('order_items')
    # for product in query_set:
    #     for order_item in product.order_items.all():
    #         # print(order_item) # OK
    #         print(order_item.quantity) # حتی اینم بدون مشکل
    # و تعداد کوئری ها از ۱۰۰۳ به ۴ عدد میرسه. دقت کنم که ۱۰۰۰ تا کم نشد.
    # ۹۹۹ تا کم شد. دلیلیش اینه که این دیگه مثل سلکت ریلیتد از اینر جوین استفاده نمیکنه.
    # به جاش اولی یه بار تمام آی دی های لازم رو میگیره و بعد از یه کوئری دیگه با اپراتور
    # IN استفاده میکنه. دقیقا مثل همون تمرینات قبلی بود که خود حاجی حسینی میومد چند
    # تا کوئری استفاده میکرد. اول یه کوئری برای چیزی مینوشت و بعد دومی رو میگفت
    # اونهایی که آیدیشون تو این هستند. اینجا خود جنگو این کار رو برای ما میکنه.
    # خلاصه مطلب در مورد اینا اینه که اگه مدلمون به یه چیزی فارین کی زده باشه،
    # برای این که هیچ کوئری اضافه ای نزنیم و الکی ۱۰۰۰ بار درخواست ندیم به دیتابیس،
    # از متد سلکت ریلیتد استفاده میکنیم و داخلش اسم اون فیلدی که فارین کی هست رو مینویسیم
    # اگه مدلی که داریم استفاده میکنیم، یه چیز دیگه بهش فارین کی زده باشه و ریلیتد نیم
    # داشته باشه، با استفاده از متد پریفچ ریلیتد و نوشتن اسم ریلیتد نیم داخلش،
    # باعث میشیم که خودش یه کوئری اضافه بزنه و بره آیتم هایی که مربوط به اون هستند رو
    # ساده تر بیاره. و یه کوئری جدا اضافه میکنه که خب خیلی بهتر از ۱۰۰۰ تاست.
    
    #############################################################################
    ############################# تمرین های سری دوم فصل ORM & queries. در حال حاضر فایل ۳۴۳ 
    #############################################################################
    # #11 تمام کامنت ها رو بگیر. (اسم کامنت گذار) + اسم محصولی که براش کامنت گذاشته شده
    # #11 و همچنین وضعیت کامنت که تایید شده هست یا نیست یا در انتظار تایید هست.
    # query_set = Comment.objects.select_related('product')
    # for comment in query_set:
    #     print(comment.name, comment.status, comment.product.name)
    # context.update(
    #     {
    #         'comments': query_set,
    #     }
    # )

    # #12 برای تمام محصولات، کامنت هاش رو نشون بده. (کامنت آی دی هاشون رو هم نشون بده)
    # query_set = Product.objects.prefetch_related('comments')
    # for product in query_set:
    #     print(f"Prdouct: {product.name}", end='. ')
    #     for comment in product.comments.all():
    #         print(f"Comment number: {comment.id}, Comment body: {comment.body}")
    #     print('-'*100)
    # context.update(
    #     {
    #         'products': query_set,
    #     }
    # )

    # #13 برای تمام محصولات، کامنت هاش رو نشون بده. عنوان کتگوری اش رو هم نشون بده
    # query_set = Product.objects.prefetch_related('comments').select_related('category')
    # for product in query_set:
    #     print(f'Product: {product.name}. Category: {product.category.title}\nComments:')
    #     for i, comment in enumerate(product.comments.all()):
    #         # print(f"comment id {comment.id}: {comment.name} said: {comment.body}")
    #         print(f"{i+1}: {comment.name} said: {comment.body}") # اینم اشانتیون واسه خودم انجام دادم😁
    #     print('-'*100)
    # context.update(
    #     {
    #         'products': query_set,
    #     }
    # )

    # #14 برای تمام سفارشات، لیست اردرآیتم ها رو بگیرید و آی دی اردرآیتم ها رو نمایش بدید
    # #14 علاوه بر این، اسم کوچیک کاستومری که اردر رو داده رو هم نمایش بدید.
    # query_set = Order.objects.all().prefetch_related('items').select_related('customer')
    # for order in query_set:
    #     print(f"Customer: {order.customer.first_name}. Order Items:")
    #     for order_item in order.items.all():
    #         print(order_item.id, end=', ')
    #     print('\n', '-'*60)
    # context.update(
    #     {
    #         'orders': query_set,
    #     }
    # )

    # #15 برای تمام سفارشات، لیستی از نام محصولات سفارش داده شده را به همراه
    # #15 نام سفارش دهنده بنویسید.
    # query_set = Order.objects.all().prefetch_related('items').select_related('customer') # این طوری دوباره کنده
    # query_set = Order.objects.all().prefetch_related('items__product').select_related('customer') # این طوری سریع میشه
    # for order in query_set:
    #     print(f"Customer: {order.customer.first_name}. Order Items:")
    #     for i, order_item in enumerate(order.items.all()):
    #         print(f"#{i+1}: {order_item.product.name}", end=', ')
    #     print('\n', '-'*60)
    # context.update(
    #     {
    #         'orders': query_set,
    #     }
    # )
    #############################################################################
    ############################# پایان تمرین های سری دوم فصل ORM & queries
    #############################################################################

    # aggregation
    from django.db.models import Count, Sum, Avg, Max, Min, Variance, StdDev
    # query_set = Product.objects.aggregate(Count('id')) # SELECT COUNT(`store_product`.`id`) AS `id__count` FROM `store_product`
    # query_set = Product.objects.aggregate(Count('unit_price')) # SELECT COUNT(`store_product`.`unit_price`) AS `unit_price__count` FROM `store_product`
    # query_set = Customer.objects.aggregate(Count('birth_date')) # SELECT COUNT(`store_customer`.`birth_date`) AS `birth_date__count` FROM `store_customer`
    # query_set = Customer.objects.aggregate(Count('id')) # SELECT COUNT(`store_customer`.`id`) AS `id__count` FROM `store_customer`
    # اینا ۴ تا مثال مختلف بود برای شمردن چیزی. دقت کنم که اگه ستونی نال باشه، اون رو نمیشماره. به خاطر همین
    # بهتره برای شمارش از آی دی استفاده کنیم که اغلب اوقات کلید اصلی هست و نال نیست. مگر این که اون تیبل
    # آی دی نداشته باشه. اما به هر حال اولین نوع از اگرگیت ها شمارش هست که چون زیاد استفاده میشد، یه متد
    # به اسم count هم براش گذاشتن که رو کوئری ستمون میتونیم اجراش کنیم. اما اگرگیشن اصلی خودش رو هم داره
    # که این شکلی ازش استفاده کردیم. بقیه هم الان مثال میزنم که از اسمشون معلومه خیلی توضیح نمیدم.
    # query_set = OrderItem.objects.all().aggregate(Sum('id')) # SELECT SUM(`store_orderitem`.`id`) AS `id__sum` FROM `store_orderitem`
    # که رو آی دی زدم و به درد لای جرز میخوره 😂
    # query_set = OrderItem.objects.all().aggregate(Sum('unit_price')) # SELECT SUM(`store_orderitem`.`unit_price`) AS `unit_price__sum` FROM `store_orderitem`
    # پول کل محصولاتی که فروختیم که یه چیز خیلی منطقی هست
    # query_set = Product.objects.all().aggregate(Avg('unit_price')) # SELECT AVG(`store_product`.`unit_price`) AS `unit_price__avg` FROM `store_product`
    # میانگین قیمت محصولات سایتمون
    # خودم یه کم فضولی کردم تو فایلش دیدم که واریاس و انحراف معیار هم داره که فکر نکنم به کار بیاد.
    # اما شیوه استفاده ازشون آسون بود و اینجا نوشتم. مثلا بعدی واریاس قیمت محصولات فروخته شده رو میده 😁
    # query_set = OrderItem.objects.all().aggregate(Variance('unit_price')) # SELECT VAR_POP(`store_orderitem`.`unit_price`) AS `unit_price__variance` FROM `store_orderitem`
    # این یکی هم انحراف معیار 🤦‍♂️😁
    # query_set = OrderItem.objects.all().aggregate(StdDev('unit_price')) # SELECT STDDEV_POP(`store_orderitem`.`unit_price`) AS `unit_price__stddev` FROM `store_orderitem`
    # البته نگاه کردم خود دیتابیس ها اغلب همچین چیزی رو دارن و این طور نیست که جنگو اضافه کرده باشه
    # اما کد ارتباطش رو با دیتابیس نوشته. خلاصه بریم ادامه دوره حاجی حسینی
    # یک شیوه دیگر برای گرفتن قیمت گرانترین محصول و ارزانترین
    # query_set = Product.objects.all().aggregate(Max('unit_price')) # SELECT MAX(`store_product`.`unit_price`) AS `unit_price__max` FROM `store_product`
    # query_set = Product.objects.all().aggregate(Min('unit_price')) # SELECT MIN(`store_product`.`unit_price`) AS `unit_price__min` FROM `store_product`
    # البته دقت کنم که این اگرگیشن ها فقط مقدار رو میدنا. مثلا الان فهمیدیم که قیمت ارزونترین محصول چیه
    # اما اگه بخوایم تو سایت نشون بدیم یا اطلاعات دیگه شو ببینیم چیزی به ما نمیده و از همون متدهایی که
    # یاد گرفتیم باید استفاده کنیم تا کل اون آبجکت رو بگیریم. اما اگه جایی فقط تعداد یا حاصل جمع یا ماکسیمم
    # یا ... چیزی برامون مهم بود و نه کل خود اون آبجکت، استفاده از اگرگیشن ها سرعت رو بالاتر میبره.
    # حالا میرسیم قسمت جذاب ماجرا. اسمی که خودش میذاره کار کردن باهاش سخته. ما میتونیم به صورت kwarg
    # به متد اگرگیت مقدار بدیم و اسمی که ما بهش میدیم رو برای جواب میذاره. جدای از اون میتونیم همزمان
    # چند مورد رو هم درخواست بدیم و همه رو بهمون به صورت یک دیکشنری میده. دقت کنم که باز آبجکت نیست و دیکشنری
    # هست. اما خب این مدلی خیلی به درد بخور تره. مثلا الان من میخوام ببینم که ارزون ترین محصولی که دارم و گرون ترین
    # قیمتشون چنده؟ همچنین میخوام تعداد محصولات رو بدونم و میانگین قیمتشون رو هم بدونم. با کوئری زیر
    # و جالب اینجاست که همه رو با یه کوئری برای من میگیره و میاره. عمدا اسم ها رو فینگلیش یا کامل نوشتم
    # که یادم باشه هر چی دلم بخواد میتونم بنویسم.
    # query_set = Product.objects.all().aggregate(
    #     min=Min('unit_price'),
    #     max=Max('unit_price'),
    #     tedad=Count('id'),
    #     average=Avg('unit_price'),
    #     ) # SELECT MIN(`store_product`.`unit_price`) AS `min`, MAX(`store_product`.`unit_price`) AS `max`, COUNT(`store_product`.`id`) AS `tedad`, AVG(`store_product`.`unit_price`) AS `average` FROM `store_product`
    # نکته آخر این که اگه آل رو هم نمینوشتم، به صورت پیش فرض خودش رو کل تیبل اون کوئری رو میزنه. اما میتونیم
    # تغییرش هم بدیم. مثلا همین چیزهای بالا رو الان میخوام برای ۳۰۰ محصول گرانتر پیدا بکنم.
    # query_set = Product.objects.order_by('-unit_price')[:300].aggregate(
    #     min=Min('unit_price'),
    #     max=Max('unit_price'),
    #     tedad=Count('id'),
    #     average=Avg('unit_price'),
    # ) # SELECT MIN(`__col1`), MAX(`__col1`), COUNT(`__col2`), AVG(`__col1`) FROM (SELECT `store_product`.`unit_price` AS `__col1`, `store_product`.`id` AS `__col2` FROM `store_product` ORDER BY `store_product`.`unit_price` DESC LIMIT 300) subquery
    # این نکته ربطی به جنگو نداره و مال مای اس کیو ال هست. خواستم دستورش رو تست کنم اون سابکوئری آخر
    # رو برداشتم ارور میداد و Every derived table must have its own alias
    # یعنی هر جدول مشتق شده باید نام مستعار خود را داشته باشد
    # یه اسم الکی گذاشتم مثل a و b و s‌ و اینا و دیگه ارور نمیداد. اما داخل اون جدول های موقتی که درست کرد،
    # مثل این که حتما باید اسم مستعار تعریف کنیم. خلاصه این که کل این خواسته هام رو با فقط یک کوئری به من داد.

    # تمرین: تعداد و میانگین قیمت محصولاتی که تعداد اینونتوری شون بیشتر از ۱۰ تاست رو تحویل بدید
    # query_set = Product.objects.filter(inventory__gt=10).aggregate(
    #     amount=Count('id'),
    #     average=Avg('unit_price'),
    # )

    # تمرین: چند تا اردرآیتم هستند که به پروداکت ۱ وصل هستند. از نظر منطقی یعنی محصول ۱ تو چند تا آردر آیتم هست
    # چون جوابش صفر بود، خودم محصول ۹۹۳ رو در نظر گرفتم به جاش که جوابش ۴ تاست تو دیتابیس نمونه مای اس کیو ال من
    # روش ۱ که درست و اصولی هست✅
    # query_set = OrderItem.objects.filter(product=993).aggregate(
    #     amount=Count('id'),
    # )
    # روش ۲ که ۲ تا کوئری میزنه و جالب نیست
    # query_set = Product.objects.get(id=993).order_items.aggregate(
    #     amount=Count('id')
    # )
    # روش ۳ که باز هم ۲ تا کوئری میزنه و جالب نیست و (دیکشنری هم به ما نمیده یه عدد صحیح میده فقط.)
    # query_set = Product.objects.get(id=993).order_items.all().count()
    # تمرین خیلی جالبی بود ها. به راحتی میتونیم بفهمیم هر محصول چند تا فروش داشته

    # تمرین: چند تا محصول هستند که داخل هیچ اردری نیستند؟ مثلا میخوایم محصولاتی که فروش نرفتند رو پیدا
    # کنیم دیگه اون محصولات یا مشابهشون رو نیاریم الکی. چون کسی اونا رو نمیخره 😁
    # خب اول محصولاتی رو پیدا میکنیم که حداقل داخل یه اردر آیتم بودند
    # query_set_order_items = OrderItem.objects.values('product').distinct()
    # دقت کنم که اینجا نباید آل رو بگیرم. در واقع اول با آل نوشتم و دیدم که جواب اشتباهه. چرا؟
    # چون وقتی آل میزنم، کل اردرآیتم ها رو بهم میده که خب هر کودومشون یک نمونه از کلاس اردرآیتم هستند.
    # پس عملا دیستینکت روشون معنی نداره. چون حتی اگه همه فیلدها شون هم مثل هم باشه، حداقل آی دی هر کودوم
    # فرق داره و یک این باعث میشه که عملا دیستینکت بیخود بشه. دیستینکت رو معمولا روی متد ولیوز یا ولیوزلیست
    # صدا میکنیم. چون که اونا یه چیز مجموعه طور به ما میدن که عضو تکراری ممکنه توشون باشه. اما وقتی من آل رو
    # صدا کردم یا مثلا فیلتر رو صدا میکنیم، اینها خود آبجکت ها رو میدن که عملا دیستینکت زدن روشون بی فایده هست.
    # خلاصه این که اینجا به جای ولیوز، ولیوز لیست رو هم میشد نوشت و کار میکرد و مشکلی نبود. اما خودش ولیوز رو
    # نوشت. من هم همین رو مینویسم. نکته دیگه این که خودش product_id ها رو گرفت. اما چون فارین کی بود و چند بار
    # تا حالا نوشتم، خود product یا product__id رو هم میشه نوشت و هر ۳ مورد رو تست کردم جواب درست رو میداد.
    # خب تو مرحله بعد، میریم سراغ محصولاتی که جزو این دسته بالایی ها نیستند و تعدادشون رو میشماریم 
    # روش اول جهت مرور و یادآوری کیو آبجکت و استفاده از نات
    # from django.db.models import Q
    # query_set = Product.objects.filter(~Q(id__in=query_set_order_items))
    # روش دوم جهت استفاده از متد اکسکلود که خودش نات میکرد.
    # query_set = Product.objects.exclude(id__in=query_set_order_items)
    # حل سوال تمام شد. اما برای چالش بیشتر، به این صورت هم مینویسم که بدونم میشه
    # query_set = Product.objects.exclude(id__in=OrderItem.objects.values('product').distinct())
    # یا
    # from django.db.models import Q
    # query_set = Product.objects.filter(~Q(id__in=OrderItem.objects.values('product').distinct()))
    # که همه مواردی که گفتم یه خروجی دارن. صرفا جهت تمرین بیشتر بود. چون اینا چیزایی بود که کمتر
    # روشون کار کرده بودم.

    # تمرین: چه تعداد محصول داریم که در سال ۲۰۲۲ فروش رفتند؟
    # خودش حل نکرد. اما گفت کَونت میزنیم روش. فکر کنم منظورش این بود که کلا از چه جنس محصولی فروختیم
    # اما من فکر کردم منظورش کل تعداد محصولات فروخته شده هست. به هر حال هر دو تا رو گفتم بده به ما و این میشه
    # query_set = OrderItem.objects.filter(order__datetime_created__year=2022).aggregate(
    #     sold_products=Count('quantity'),
    #     sum_of_all_each_single_products_sold_of_all_of_these_pdoduct_types_donoghte_di=Sum('quantity'),
    #     )
    # print(query_set)

    # annotation
    # کلا انوتیشن یعنی این که یه فیلدی رو موقع گرفتن اطلاعات به تیبلمون اضافه کنیم. در حالی که اطلاعاتش
    # واقعا تو اون تیبل نیستند و وجود ندارند. اما موقع گرفتن اطلاعات به جای این که خودمون محاسبه کنیم،
    # محاسبات رو بسپاریم به دیتابیس.
    # برای توضیح انوتیشن، یه توضیح کوتاه بدم که یه چیزی داریم به اسم اکسپرشن
    # expression
    # تو جنگو به ۵ دسته تقسیم میشن که اگرگیشن یه مدلش بود که اگرگیشن ها رو یاد گرفتیم.
    # یه مدل دیگه اش Value هست که یه مقدار ثابت میتونیم بهش بدیم.
    # سه مدل دیگه هم داره که تا همینجا کافیه. فقط اسم هاشون رو اینجا مینویسم
    # Value
    # F
    # Func
    # Aggregate
    # ExpressionWrapper
    # برای توضیحش از مثال استفاده میکنیم.
    # مثلا ما موقعی که از تیبل محصولات اطلاعات اونا رو میگیریم، فیلدی به اسم قیمت و فیلدی به اسم تعداد داریم
    # اما مثلا میخوایم ببینیم که ارزش قیمتی از کل تعداد محصولات یک محصول هم که داریم چقدره. مثلا یه محصول داریم
    # هزار تومان و ده تا ازش داریم. ارزش کل اونا میشه ده هزار تومان. یه محصول دیگه داریم صد تومان و صد تا
    # ازش داریم. ارزش کل اینا هم میشه ده هزار تومان. میخوایم این مدلی ارزش کل همه محصولات رو هم بگیریم.
    # در حالی که تو تیبل دیتابیس همچین فیلدی رو نداریم. میتونیم تولید بکنیم.
    # این میشه کلیت انوتیشن که الان کدش رو هم میبینیم. فقط قبل از این که همینی که گفتم رو ببینیم، یه مدل ساده تر
    # از اکسپرشن ها رو هم میبینیم. چون وسط نوشتن مثال به کارمون میاد. اولیش مثلا همین ولیو هست که یه ستون جدید
    # میتونیم با مقدار ثابت مشخص اضافه کنیم
    from django.db.models import F, Value, Func, ExpressionWrapper
    # query_set = Product.objects.all().annotate(alaki=Value('salam'), alaki2=Value(3))
    # این جا مثلا ۲ تا ستون جدید اضافه کردیم که یکیش همه جا سلام هست و اون یکی ۳ و اسم دلخواه هم براشون گذاشتیم.
    # به چه کاری میاد؟ تو مثال بعدی نه. بعد از اون میبینیم. مثلا میخوایم مالیات رو هم حساب کنیم اونجا
    # query_set = Product.objects.all().annotate(total_price=F('unit_price')*F('inventory'))
    # print(list(query_set))
    # تو این مثال از اف آبجکت استفاده کردیم که قبلا هم نمونه اش رو دیدیم و نوع دوم از انوتیشن ها هست.
    # اینجا حاصل ضرب ۲ تا از ستون ها رو میده به ما
    # تو مثال بعدی میخوایم مثلا مالیاتش رو هم حساب کنیم و ضربدر ۱.۱ کنیم. اما دقت کنم که نمیتونه فلوت و دسیمال
    # رو تو هم ضرب کنه. پس از دسیمال پایتون استفاده کردم. از طرفی، عدد رو هم نمیشه به صورت ساده نوشت. پس از ولیو
    # هم اینجا استفاده میکنیم به خاطر همین هست که ولیو رو قبلش گفتیم
    # البته بدون ولیو هم تست کردم کار میکرد.😁 اما خب به هر حال گذاشتم باشه.
    # from decimal import Decimal
    # query_set = Product.objects.all().annotate(total_price=F('unit_price')*F('inventory'), total_price_with_tax=F('total_price')*Value(Decimal(1.1)))
    # for product in query_set:
    #     print(product.total_price, round(product.total_price_with_tax, 4))
    # البته این روش خودم بود که دسیمال اضافه کردم و مشکل حل شد. اما اگه نبود این ارور رو میداد
    # Cannot infer type of '*' expression involving these types: DecimalField, FloatField. You must set output_field.
    # من همین که دیدم دسیمال و فلوت رو نمیشه تو هم ضرب کرد از دسیمال پایتون استفاده کردم. اما ارورش میگه که من
    # نمیدونم حاصل ضرب دسیمال و خروجی رو با چه دقتی ذخیره کنم. بایت فیلد خروجی رو بهم بگی. اینجا هست که از مدل
    # آخر اکسپرشن رپر استفاده کرد. اما خب به هر حال ما منم روشی هست دیگه. به آخر که رسیدیم اکسپرشن رپر
    # رو هم سر همین مثال توضیح میدم. چون چیز کم کاربردی هست و حالا که مثالش رو دارم، سر همین توضیح میدم اون رو
    # اما فعلا بریم سراغ مهم تر ها.
    # Func مدل سوم
    # برای استفاده از تابع های دیتابیس هست. مثال این رو روی مشتری ها میزنیم. مثلا میخوایم اسم کامل مشتری ها رو بگیریم
    # query_set = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    # بعد از کلاس فانک، اول ورودی ها رو هر چقدر که هستند میدیم و آخر سر تابع دیتابیس رو با کیوورد آرگومان فانکشن بهش اعلام میکنیم.
    # یادآوری. اگه مثلا نخوایم دیگه اسم کوچیک و فامیلی رو بگه، از دیفر استفاده میکنیم.
    # query_set = query_set.defer('first_name', 'last_name') # این هم جالب شد دیگه کپی پیست نکردم. کوئری ها لیزی بودند دیگه رو همون قبلی زدم.
    # print(list(query_set))
    # میخوایم ببینیم هر اردری، چند تا اردرآیتم داره
    # query_set = Order.objects.annotate(item_counts=Count('items'))
    # print(list(query_set))
    # دستور ساده و جالبی داشت. اما ORM میاد از گروپ بای استفاده میکنه. دستور اس کی الش رو اینجا کپی
    # میکنم. اما اصلا مهم نیست و فقط خواستم اینجا باشه که از LEFT OUTER JOIN هم استفاده شده
    # SELECT `store_order`.`id`, `store_order`.`customer_id`, `store_order`.`datetime_created`, `store_order`.`status`, COUNT(`store_orderitem`.`id`) AS `item_counts` FROM `store_order` LEFT OUTER JOIN `store_orderitem` ON (`store_order`.`id` = `store_orderitem`.`order_id`) GROUP BY `store_order`.`id` ORDER BY NULL
    # نمیدونم چه ایرادی داره این دستور که هر بار میزنم، دفعه اول کوئری ها میشه ۵ تا که مینویسه 2 similar queries | diplicate 2 times. بعد که رفرش میکنم میشه ۲ تا کوئری که یکیش مال سشن هاست. دوباره که جنگو رو سیو میکنم میرم اونور میشه ۵ تا. و رفرش که میکنم میشه ۲ تا😁 بگذریم مهم نیست. این اتفاق برای تمرین پایین هم میفته. شاید به خاطر همین لفت اوتر جوین باشه.
    # ⭐⭐⭐⭐⭐⭐ تمرین: تعداد اردرهایی که هر کاستومر داره رو مشخص کنید ⭐⭐⭐⭐⭐⭐ 
    # query_set = Customer.objects.annotate(orders_count=Count('orders'))
    # print(list(query_set))
    # Aggregate
    # aggregation ها رو که کامل تو قسمت قبل توضیح دادیم. بریم سراغ
    # ExpressionWrapper
    # برای این استفاده میشه که بتونیم نوع خروجی اکسپرشنمون رو مشخص کنیم. اگه یادم باشه، اول بحث انوتیشن گفتیم که
    # با اکسپرشن ها سر و کار داریم و ۵ مدل رو معرفی کردیم و مدل آخر همین بود. مثال مالیات هم دیدیم که خودم به یه 
    # روش دیگه حل کرده بودم. این یکی خیلی مهم نیست. اما مثالش رو مینویسم اینجا دوباره و این بار با اکسپرشن رپر
    # انجام میدم
    # from django.db.models import DecimalField # این همون دسیمال فیلدی هست که موقع تعریف تو فایل مدلز هم استفاده میکنیم. در واقع همه اینا تو مدلز هستند.😊
    # query_set = Product.objects.all().annotate(
    #     total_price=F('unit_price')*F('inventory'),
    #     total_price_with_tax=ExpressionWrapper(F('total_price')*Value(1.1), output_field=DecimalField())
    #     )
    # for product in query_set:
    #     print(product.total_price, round(product.total_price_with_tax, 4))
    # آخرین نکته از این بخش که خیلی چیز مهمی نیست این اکسپرشن رپر فکر کنم. خود حاجی حسینی هم خیلی روش تسلط نداشت
    # به نظرم. یه چیز اتفاقی هم که دیدم، تو روش خودم تو جنگو دیباگ تولبار نمیشد خروجی ها رو دید و sel
    # براش فعال نبود. خود حاجی حسینی هم نداشت و یه بار دیگه هم که قبلا کار میکرد یه جا نبود گفته بود احتمالا
    # باگ خورده. اما این جا وقتی با اکسپرشن رپر نوشتم دیدم میاد. یعنی وقتی عادی و با روش دسیمال خودم رفتم نبود.
    # اما وقتی با اکسپرشن رپر مینویسم و میبینم هست. این نکته رو هم بنویسم که از نظر جنگو حتما روش کار کردن و چیز
    # درست نوشته شده ای هست. و به خاطر اطلاعات ناقص ما درست درکش نکردیم. اما خوب نوشته شده. با این حال چیز خیلی
    # کاربردی ای نیست که حاجی محمدی با تجربه زیادش بهش نپرداخته و تسلط نداشت زیاد روش. پس به کار من هم احتمالا
    # حالا حالا ها نمیاد. نکته آخر این که احتمالا انوتیشن ها بیشتر از ۵ مدل باشن. حاجی محمدی ۵ مدلش رو گفته.
    # ذهنم رو بسته نگه ندارم. اما اول اصلیات رو یاد بگیرم بعد برم جزییات.

    # Manager + custom manager ( + custom lookup که اینو دیگه خودم اضافه کردم)
    # وقتی موقع ساخت مدل هامون از models.Model‌ ارث بری میکنیم، خودش یه منیجر هم داره که به صورت پیش فرض، اسمش objects
    # هست. اگه بخوایم میتونیم اسمش رو هم دوباره همون بذاریم، اما ترجیحا این کار رو نکنیم و اسمی متفاوت بذاریم مثلا my_objects
    # به دو دلیل. دلیل اول این که ما داریم اون رو تغییر میدیم، اگه چند وقت دیگه خودمون نگاه کنیم یا کس دیگه ای
    # نگاه کنه و اسمش همون objects باشه که به صورت پیش فرض هست، نمیفهمه که تغییرش دادیم و گول میخوره.
    # دلیل دوم این بود که وقتی داخلش تابع اضافه میکنیم، وی اس کد چون کلمه آبجکتس رو از قبل میشناسه، متدهای
    # اون رو به ما نشون میده و موقع نوشتن اسم متدهایی که خودمون نوشتیم کمکمون نمیکنه. اما موقع نوشتن مثلا my_objects
    # کمک میکرد. خلاصه نحوه استفاده ازش اینه که تو مدلز باید یه کلاس منیجر درست کنیم که از models.Manager
    # ارث بری میکنه. داخلش تابع های جدیدی که میخوایم رو اضافه میکنیم مثل همین کامنت منیجری که درست کردیم.
    # و چون ارث بری کرده، تمام چیزهای قبلی رو هم داره. دقت کنم که وقتی یه منیجر اضافه میکنیم دیگه خودش از اون
    # استفاده میکنه و objects رو نمیشناسه و بهش ارور میده. اگه دوست داریم میتونیم یه منیجر دیگه هم تعریف کنیم
    # و اسم اون objects باشه و همون اولیه باشه. اما خب چه کاریه. مال ما که همون هست و چیزهای اضافه تر هم داره.
    # با این حال اگه یه منیجر دیگه مثل ApprovedCommentManager درست کنیم که پیش فرضش فقط Approved ها رو میاره و
    # دیگه به نات اپروود و ویتینگ دسترسی نداریم، میتونیم چند تا منیجر هم برای یه مدل تعریف کنیم.
    # کارهای مربوط به ساخت و یا تغییر و دستکاری منیجر داخل همون مدلز.پای انجام میشه که اون ور میتونم
    # نمونه ها رو برای کامنت ببینم.
    # query_set = Comment.my_objects.get_approved()
    # query_set = Comment.my_objects.get_not_approved()
    # query_set = Comment.my_objects.get_waiting()
    # print(len(query_set))
    # query_set = Comment.approved_objects.all()
    # query_set = Comment.approved_objects.filter(name__ne='Ashley') # مثال کاستوم لوکاپ از داکسِ جنگو
    # query_set = Comment.approved_objects.filter(body__length_less_than=100) # مثالی که خودم نیاز داشتم و رفتم سرچ کردم
    # print(len(query_set)) # 😊جالب شد. خودم حال کردم😊

    # تمرین: برای اردرها، ۲ تا منیجر بنویسیم. یکی منیجری که به طور کلی پرداخت نشده ها رو بگیره، یکی هم
    # منیجری که یه متد گت بای استاتوس بهش اضافه کنیم که بتونیم استاتوس رو بهش بدیم و اون مدل سفارش ها رو پیدا کنه
    # یعنی موقع کال کردن بهش بگیم که کنسل شده ها رو میخوایم یا پرداخت شده ها یا پرداخت نشده ها
    # query_set = Order.unpaid_manager.all()
    # query_set = Order.my_manager.get_by_status(status='u')
    # print(len(query_set))

    # CRUD
    # Create
    # روش ۱
    # Comment.objects.create(product_id=1, name='محمد', body='محصول جالبیه')
    # روش ۲
    # new_comment = Comment(product_id=1, name='محمد', body='محصول جالبیه')
    # یا
    # new_comment = Comment()
    # new_comment.product_id = 1
    # new_comment.name = 'محمد'
    # new_comment.body = 'محصول جدید'
    # new_comment.save()
    # روش ۲ یه کم کد اضافه تر داره. اما موقعی که میخوایم آپدیت کنیم به دردمون میخوره و از روش اول نمیشه موقع
    # آپدیت استفاده کرد. چون دقیقا تابع کریت رو صدا میکنه. اما متد سیو اگه نمونه ای که ساختیم جدید باشه، کریت
    # رو صدا میکنه و اگه از یه نمونه از دیتابیس اطلاعات رو گرفته باشیم، ویرایش میکنه.
    # Update
    # 💀 روش اول که استفاده نکنیم. خطرناکه 💀
    # category = Category(id=100)
    # category = Category(pk=100) # توصیه اش اینه که از pk اینجا استفاده کنیم
    # category.title = 'یک محصول جدید'
    # category.description = 'این محصول جدید است'
    # category.top_product_id = 2 # دقت کنم که جاهایی که فارین کی زدیم دقیقا باید همون آی دی باشه. پی کی کار نمیکنه اینجا
    # category.save()
    # این مدلی که همه چیز رو خودمون با اطمینان پر کنیم روش اول هم اوکی هست.
    # اما باید حواسمون باشه که حتما به همه چی مقدار بدیم. وگرنه هر چیزی که بهش مقدار ندیم یه استرینگ
    # خالی براش میفرسته که اگه تو دیتابیس استرینگ باشه، اطلاعاتش با استرینگ خالی جایگزین میشه و عملا پاک میشه
    # و اگه عددی و اینا هم باشه و اجباری هم باشه، میخواد توش '' بذاره که خب ارور میده.
    # خیلی وقتا ما ۶۰ تا فیلد داریم که میخوایم فقط یکی رو عوض کنیم یا مثلا ۳ ۴ تا رو که میریم سراغ روش بهتر دوم
    # 😟 روش دوم 😟
    # category = Category.objects.get(pk=100) # اینجا هم میشه از id استفاده کرد. ولی pk توصیه میشه
    # category.top_product_id = 3 
    # category.save()
    # این روش بهتر هست و مشکل ازبین بردن اطلاعات رو نداره. اما ۲ تا کوئری میزنه. یکی برای گرفتن اطلاعات از دیتابیس
    # یکی هم برای ویرایش کردن اطلاعات. تو روش سوم با یه کوئری این کار رو میکنیم.
    # 💀👍 روش سوم 👍💀
    # تو روش سوم از خود تابع آپدیت منیجر اُ آر اِم استفاده میکنیم
    # Category.objects.filter(pk=100).update(top_product_id=7)
    # این که رو پرایمری کی فیلتر بزنیم یه مورد رو تحویل میده. اما خیلی خیلی دقت کنم که اگه فیلتر نزنیم دهنمون
    # سرویس میشه. یعنی رو کل تیبل اعمال میکنه. مثل این پایینی
    # 💀 # Category.objects.update(top_product_id=10) # UPDATE `store_category` SET `top_product_id` = 10
    # اینجا چون همه نال بودند زدم همه رو گذاشت ۱۰. اما اگه اسم یا قیمت یه چیز رو بخوایم بزنیم و این اشتباه
    # رو بکنیم فاجعه است. پس همیشه حواسم بهش باشه.
    # Category.objects.filter(pk__in=[100, 97, 91]).update(top_product_id=6) # این هم با یه کوئری اجرا میشه
    # UPDATE `store_category` SET `top_product_id` = 6 WHERE `store_category`.`id` IN (100, 97, 91)
    # Delete
    # اول یه کتگوری الکی بسازم
    # Category.objects.create(title='alaki', id=101)
    # روش ۱
    # 💀 #Category.objects.filter(pk=101).delete() # چند بار تست کردم این به تنهایی ۳ تا کوئری به دیتابیس زد. البته وقتی که
    # جواب داشت. وقتی که جواب نداشت فقط یه سلکت بود که چیزی پیدا نمیکرد و خب دیگه ۲ تای دیگه رو هم نمیزد.
    # حتما حتما هم حواسم باشه اگه فیلتر رو ننویسم همه رو میزنه پاک میکنه ها
    # البته یه دیتابیس الکی ساختم و تست کردم Category.objects.delete() و خدارو شکر ارور میداد که
    # 'Manager' object has no attribute 'delete'
    # اما کرم نریزم دیگه حواسم باشه.
    # روش ۲
    # Category(pk=101).delete() # این یکی چه بود چه نبود ۲ تا کوئری میزد.
    # این رو هم Category().delete() این مدلی تست کردم و خدارو شکر این ارور رو داد
    # Category object can't be deleted because its id attribute is set to None.

    # transaction
    # این موضوع بعد از تمرین پایین بود. اما چون خودش تمرینی نداشت، من اینجا نحوه استفاده شو
    # مینویسم. برای استفاده ازش، دو شیوه هست
    # شیوه اول اینه که تابع رو اتمیک کنیم و کل تابع اون شکلی باشه یعنی برگردم به قبل از تعریف
    # تابع show_data و @transaction.atomic() رو بذارم که از دکوریتورش استفاده کنه. این طوری کل
    # عملکرد تابع رو اتمیک کردیم
    # شیوه دوم اینه که داخل تابع جایی که میخوایم، بنویسیم 
    # with transaction.atomic():
    # و بخشی از کد رو که میخوایم اتمیک باشه داخلش بنویسیم
    # تمرین رو با ترنسکشن اتمیک هم تست کردم به هر دو شیوه و درست کار میکرد
    # با دیباگ کردن تست کردم و دیدم موقعی که هر دستور ساخت دیتابیس رو میزنیم اعمال نمیشه
    # و صبر میکنه تا آخر و اگه همه چی اوکی باشه آخر سر اعمال میشه.
    # اما اگه وسطاش یکی مشکل داشت تو دیتابیس اعمال نمیشه. با این وجود تعداد کوئری ها تو هر دو
    # حالت یکسان بود و علاوه بر این وقتی بعدا درست ساختم، چند باری که اشتباه بود آی دی ها
    # که اتو اینکریمنت بودند چند واحد اضافه شده بودند. یعنی انگار عملا کاری که بهش گفتیم رو
    # انجام میده، اما وقتی اتمیک هست برعکس اون کار رو هم تو حافظه نگه میداره که وقتی به مشکل
    # خورد برعکسش رو هم انجام بده دیگه این ها رو کامنت کردم. تمرین رو عادی نوشتم اگه
    # دوست داشتم میتونم ترنسکشن رو هم قاطیش کنم

    # تمرین
    # قسمت اول مربوط به کریت
    # یک کتگوری به اسم a و با توضیحات aaaa بسازید و تاپ پروداکتش هم دلخواه باشه.
    # سپس دو محصول بسازید که کتگوری آنها همین a باشه
    # سپس یک اردر بسازید که برای کاستومر شماره ۱ هست و ۳ اردرآیتم برای آن بسازید
    # اردرآیتم ۱ ده عدد از اولین محصولی که الان ساختیم 
    # اردرآیتم ۲ بیست عدد از دومین محصولی که الان ساختیم
    # اردرآیتم ۳ سی عدد از محصول با آی دی شماره ۱
    # قیمت زمان سفارش محصولات هم همون قیمتی هست که محصولات دارند.
    # قسمت دوم مربوط به آپدیت
    # حالا عنوان کتگوری رو از a به mobiles‌ تغییر بدیم
    # قسمت سوم مربوط به دیلیت
    # در مرحله آخر همه رو پاک کنیم و به ترتیب پاک کردن هم دقت کنیم. چون به خاطر پروتکت بودن،
    # نمیذاره بعضی هاپاک شن و ترتیب پاک کردن توشون مهم هست
    # حل قسمت اول
    # with transaction.atomic():
    # new_category = Category()
    # new_category.title='a'
    # new_category.description='aaaa'
    # new_category.top_product_id=33
    # new_category.save()
    # product1=Product()
    # product1.name='P1'
    # product1.category=new_category
    # product1.slug='p-1-ya-harchizi' # نذاشتم هم خالی ساخت. منظور '' هست. نه نان
    # product1.description='ye chize alaki'
    # product1.unit_price=7.2
    # product1.inventory=100
    # product1.save()
    # product2 = Product.objects.create(name='P2', category=new_category, description='ye chize dg alaki:D', unit_price=75, inventory=200)
    # order = Order.objects.create()
    # order_item1 = OrderItem.objects.create(order=order, product=product1, quantity=10, unit_price=product1.unit_price)
    # order_item2 = OrderItem.objects.create(order=order, product=product2, quantity=20, unit_price=product2.unit_price)
    # product3=Product.objects.get(pk=1) # اینجا چون قیمتش رو هم لازم داریم، خود آبجکت رو گرفتیم یعنی برای قیمت لازم بود که بگیریمش
    # order_item3 = OrderItem.objects.create(order=order, product=product3, quantity=30, unit_price=product3.unit_price)
    # یا
    # order_item3 = OrderItem.objects.create(order=order, product_id=1, quantity=30, unit_price=product3.unit_price)
    # اما همون طور که گفتم، دادن آی دی کوئری رو کم نمیکنه. چون برای قیمت دوباره باید از تیبل بگیریم پروداکت با آی دی ۱ رو
    # حل قسمت دوم
    # Category.objects.filter(title='a').update(title='mobiles')
    # حل قسمت سوم
    # به روش های مختلف پاک کردیم که مرور بشه
    # OrderItem.objects.filter(order_id=31).delete()
    # Order.objects.filter(id=31).delete()
    # Product.objects.filter(name__in=('P1', 'P2')).delete()
    # Category.objects.latest('id').delete()
    
    # django shell
    # خیلی مهم نیست. اما اگه خواستیم تو محیط ترمینالی بدون ران کردن بروزر و غیره
    # جنگو رو اجرا کنیم، جایی که فایل manage.py پروژه هست، دستور زیر رو مینویسیم
    # py manage.py shell
    # این طوری مثل پایتون عادی باز میشه. با این تفاوت که به پروژه جنگو ما هم دسترسی داره
    # مثلا میتونیم مدل ها مون رو ایمپورت کنیم و نمونه بسازیم یا آپدیت و پاک کنیم یا همونجا
    # کوئری بزنیم که تمام فلان محصولات رو به ما بده و غیره که یه مدلش رو مینویسم. مثلا
    # from store.models import Category
    # با این دستور کتگوری رو ایمپورت کردم
    # Category.objects.all() # همه کتگوری ها رو میده
    # Category.objects.latest('id').title # تایتل آخرین کتگوری رو میده
    # و این که میشه اینجا کارها رو انجام داد دیگه

    # اجرای دستور خام اس کیو ال  raw SQL
    # خیلی بخش مهمی نیست. در عین حال بسیار هم آسون هست.
    # سه روش برای اجرای خام دستورات داریم.
    # روش ۱
    # query_set = Product.objects.raw("SELECT id, name, unit_price FROM store_product WHERE unit_price<10;")
    # print(list(query_set))
    # مشکلی که داشت، این بود که id رو ننوشتم. اما بهم ارور میداد که Raw query must include the primary key
    # با این حال کلک زدم و از مدل پروداکت، به منیجرش گفتم تایتل تمام کتگوری ها رو بده، گیر نداد و اجرا کرد
    # query_set = Product.objects.raw("SELECT id, title FROM store_category;")
    # روش ۲
    # from django.db import connection
    # cursor = connection.cursor()
    # cursor.execute('SELECT name, unit_price FROM store_product WHERE unit_price<10;')
    # result = cursor.fetchall()
    # print(result)
    # که تو این دیگه کامل اس کیو ال خام میزنیم و مثل پای مای اس کیو ال یا مای اس کیو ال کانکتور
    # میتونیم هر دستوری بنویسیم. مثلا همینجا دیگه من آی دی رو نگرفتم یا مثلا دیتابیس رو با دستور
    # زیر ساختم
    # cursor.execute('CREATE SCHEMA alaki_db;')
    # مثلا میتونیم برای این که تو پروژه مون نریم تو ورک بنچ یا از ترمینال دیتابیس بسازیم، یه
    # یو آر ال بسازیم که وقتی رفتیم توش دیتابیس رو بسازه و بعد تو تنظیمات بگیم که اسم دیتابیسمون
    # یعنی متغیر NAME تو ستینگز.پای اون هست. تست کردم دیدم جواب میده. اما الکی وقتم رو نگیرم.
    # چون اگه وجود نداشته باشه و بنویسیم ارور میده. بعد باید بریم اونجا بگیم که فقط به دیتابیس
    # وصل شه و اسم دیتابیس ندیم. بعد یو آر ال بسازیم که دیتابیس رو بسازه. بعد بریم تو ستینگز
    # تغییر بدیم و کی میره این همه راهو. فقط گفتم که میشه اما اصلا عقلانی نیست.
    # مهمترین نکته روش ۲ اینه که یادمون نره که کرسر رو ببندیم.
    # cursor.close()
    # اگه نبندیم خطرناک میشه که برای رفع این مشکل میشه از روش ۳ استفاده کرد با اپراتور with
    # روش ۳
    # from django.db import connection
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT name, unit_price FROM store_product WHERE unit_price<10;')
    #     result = cursor.fetchall()
    #     print(result)
    # و خودش کرسر رو میبنده
    # آخرین نکته این بخش اینه که برای کال کردن پروسیجرهای دیتابیس هم میشه از دستور زیر استفاده کرد
    # from django.db import connection
    # with connection.cursor() as cursor:
    #     cursor.callproc('esme procedure', 1, 2, 3, 'a', 'b', 'parametr ha be soorate tartibi')
    # شبیه تابع هست. منتهی باید نوشته بشه برای دیتابیس مورد نظر که بشه صداش کرد.

    # prefetch_related مبحث ویژه
    # query_set = Order.objects.all().prefetch_related('items').annotate(items_count=Count('items'))
    # for order in query_set:
    #     print(order.items_count)
    # تا اینجا که اوکی بود. حالا ما میخوایم برای هر آیتم به صورت واقعی بریم سراغ اردر آیتم هاش
    # یعنی اسمشون رو میخوایم. توضیحاتش رو میخوایم. برای لینک دادن بهش مثلا اسلاگش رو هم میخوایم
    # و غیره که میشه این شکلی
    # query_set = Order.objects.all().prefetch_related('items').annotate(items_count=Count('items'))
    # for order in query_set:
    #     for order_item in order.items.all():
    #         print(order_item.product.name, order_item.product.slug)
    # که این جوری دوباره میشه کلی هیت به دیتابیس
    # روش اول اصلاح
    # در واقع اگه بخوایم رو یه چیزی که پریفچ ریلیتد شده سلکت ریلیتد بنویسیم، دیگه
    # نمیایم از متدش استفاده کنیم و با نوشتن دو تا آندراسکور و نام اون فارین کی ای که میخوایم
    # اون رو میگیریم و این طوری خود اُ آر اِم جنگو با جوین مناسب بهینه سازی میکنه.
    # query_set = Order.objects.all().prefetch_related('items__product').annotate(items_count=Count('items'))
    # for order in query_set:
    #     for order_item in order.items.all():
    #         print(order_item.product.name, order_item.product.slug)
    # اما اگه نخوایم این شکلی بنویسیم، از کلاس پریفچ استفاده میکنیم
    # روش ۲
    # from django.db.models import Prefetch
    # query_set = Order.objects.all().prefetch_related(
    #     Prefetch(
    #         'items',
    #         queryset=OrderItem.objects.select_related('product')
    #     )).annotate(items_count=Count('items'))
    # for order in query_set:
    #     for order_item in order.items.all():
    #         print(order_item.product.name, order_item.product.slug)
    # شاید ظاهرش یه کم پیچیده تر باشه. اما خودم دفعه دومی که دیدم نسبت به دفعه اول خیلی خیلی
    # قابل درک تر بود و حتی به نظرم قشنگ هم هست. اگه کوئری هامون پیچیده تر بشه، این طوری
    # منظم تر میشه. به هر حال اینجا نوشتم که در زمان لازم به کارم بیاد.
    #############################################################################
    #############################################################################
    #####################       End Advanced Queries       ######################
    #############################################################################
    #############################################################################

    return render(request, 'store/home.html', context)