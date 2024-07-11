from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cart, CartItem, Category, Comment, Customer, Discount, Order, OrderItem, Product
from .serializers2 import AddCartItemSerializer, CartItemSerializer, CartSerializer, CategorySerializer, CommentSerializer, CustomerSerializer, DiscountSerializer, OrderCreateSerializer, OrderForAdminSerializer, OrderSerializer, OrderUpdateSerializer, ProductSerializer, UpdateCartItemSerializer
from .filters import ProductFilter
from .paginations import ProductPagination
from .permissions import CustomDjangoModelPermissions, IsAdminOrReadOnly, SendPrivateEmailToCustomerPermission, IsAdminUserOrWhoHasOrdered

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
    
    # permission_classes = [DjangoModelPermissions]
    # وقتی وارد کد همین جنگو مدل پرمیشن میشیم، میبینیم که برای اضافه کردن و تغییر و پاک کردن،
    # کدی نوشته که باید اونها رو داشته باشه طرف تا بتونه تغییر بده. اما برای گرفتن اطلاعات مشکلی
    # نیست و همه میتونن اطلاعات رو بگیرن که خب طبیعی هم هست. اما به هر حال اگه ما بخوایم که برای
    # خووندن اطلاعات هم پرمیشن بدیم به طرف که مثل پرمیشن های دیگه باشه و R از تو CRUD جدا نباشه،
    # کلاس کاستوم جنگو مدل پرمیشنز رو تعریف کردیم تو پرمیشنز .پای و از رو کدهای خودشون اومدیم
    # برای خووندن اطلاعات هم گفتیم که باید اون پرمیشن رو داشته باشه. پس از گذاشتن این، اگه کسی
    # اون پرمیشن رو نداشته باشه نمیتونه اطلاعات رو هم بخوونه. تاکید آخر که ادمین به صورت پیش فرض
    # تمام پرمیشن ها رو داره.
    permission_classes = [CustomDjangoModelPermissions]

    
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
    # میخوایم کاربرهای معمولی دسته بندی ها رو ببینن. اما نتونن پاک یا ویرایش کنن یا خودشون دسته بندی
    # اضافه کنند. اینی که الان زیر نوشتم، ادمین باشه میتونه همه کار بکنه. اما بقیه حتی نمیتونن ببینن.
    # permission_classes = [IsAdminUser]
    # حالا ما میخوایم کاستوم پرمیشن درست کنیم. مثلا اسمش رو میذاریم IsAdminOrReadOnly
    # که اگه طرف فقط برای خووندن اطلاعات اومده بود بتونه ببینه. یعنی متدهای امن گت و آپشنز و هد
    # اما پوت و پچ و پست و دیلیت دسترسی نداره. یا این که ادمین بود. ادمین بود همه کار میتونه بکنه.
    # تو فایل پرمیشنز.پای ای که ساختیم، درستش میکنیم و اینجا بهش میگیم که پرمیشن کلسش اونه
    # یا اگه چند تا هستند لیست پرمیشن ها رو بهش میدیم.
    permission_classes = [IsAdminOrReadOnly]

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


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete'] # این طوری دیگه نمیذاریم پوت بکنه 😂
    # بر خلاف کارت ویو ست که از چند چیز ارث بری کردیم، این مدلی نوشتن هم قشنگ تر و هم ساده تر و
    # هم اصولی تره. اما به هر حال گذاشتم که داشته باشم و مفهومی کار کنم به قول خودش.
    # http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

    def get_queryset(self):
        cart_pk = self.kwargs.get('cart_pk')
        return CartItem.objects.filter(cart_id=cart_pk).select_related('product')
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        if self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_pk': self.kwargs.get('cart_pk')}

# class CartViewSet(ModelViewSet):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()
# نمیخواستیم که بشه آپدیت و دیلیت انجام داد. پس به جای مدل ویو ست که از ۶ چیز ارث بری میکرد،
# اون هایی که میخواستیم رو آوردیم و اضافه کردیم. برای این که کسی نتونه کل سبدهای خرید رو هم ببینه،
# لیست رو هم نیاوردیم یعنی الان که وارد لینک مربوط به لیست ویوش میشیم میگه اجازه نداری ببینی
# اما میتونیم بسازیم. وارد جزییات یه دونه تک سبد خرید میتونیم بشیم. دیلیت و آپدیت هم نداره با
# توجه به ۳ کلاسی که ایمپورت کردیم.
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all().prefetch_related('items__product')

    # این برای این بود که اگه کسی تو یو آر ال دستکاری میکرد تو زمان ضبط فیلم بهش ارور میداد
    # و خودش رجکس تعریف کرده بود. اما مال من ارور نمیداد. خودش هم به عنوان مطلب اضافه گفته بود
    # و آخرش پاک کرده بود. خلاصه این وقتی این رو گذاشتیم اگه اون یو یو آی دی ۳۲ کاراککتری مبنای ۱۶
    # نبود صفحه ۴۰۴ رو برمیگردوند. الان خودش تو آپدیت های جنگو و بقیه پکیج ها درست شده و لازم نیست
    # نوشته بشه.
    # lookup_value_regex = '[0-9a-fA-F]{8}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{12}'


class CustomerViewSet(ModelViewSet):
    serializer_class=CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser] # این پرمیشن کلس برای کل کلاس کاستومر ویو ست اعمال میشه. 
    # خب این طوری طرف نمیتونه وارد یو آر ال (می) هم بشه. موقع تعریفش میتونیم اوجا اورایدش کنیم
    # و بگیم که اونجا پرمیشن کلسش فرق داره که اینجا این کار رو کردیم.
    # در واقع بهش گفتیم که اگر ادمین بود میتونه همه رو ببینه. ولی اگه خواست بره تو صفحه خودش
    # کافیه که آثنتیکیت کرده باشه و فقط لاگین باشه.

    # این ویوست رو درست کردیم و تو یو آر الی که ساختیم، هم لیست ویو و هم دیتیل ویو داره.
    # ولی من نمیخوام با customers/2/ برم به پروفایل. بحث این که هر کس صفحه خودش رو ببینه بعدا
    # درست میکنیم. اما میخوایم الان یه یو آر ال درست کنیم که هر کست نوشت
    # customers/me
    # اون رو به صفحه خودش ببره و اطلاعات خودش رو ببینه.
    # باز هم میگم الان همه میتونن تو
    # customers
    # اطلاعات همه رو ببینن که درستش میکنیم. تو
    # customers/id
    # هم که بزنن اطلاعات تک نفر رو میبینن. اما یو آر آل دلخوای نداریم که داخل ویوست ها این طوری
    # میتونیم یو آر ال درخواه خودمون رو تعریف کنیم. اسم تابع رو خودمون دلخواه میذاریم
    # و دکوریتور اکشن رو قبل از تعریف تابع مینویسیم. چون اسمش رو گذاشتیم می، پس بعد از تعریف
    # این تابع در زیر، میتونیم به یو آر ال customers/me بریم
    from rest_framework.decorators import action
    # فقط دقت کنم که دکوریتور اکشن، خودش ارور میداد و میگفت که حتما دیتیل رو به عنوان ورودی میخواد
    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method=='GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    # حال میخوایم کاستوم پرمیشن رو روی پرمیشنی که خودمون تعریف کرده بودیم اعمال کنیم.
    # مثلا برای ارسال ایمیل شخصی یه دونه پرمیشن خودمون ساخته بودیم دیگه. حالا میخوایم یو آر الش
    # رو درست کنیم و به کسی که این اجازه رو داره دسترسی ارسال ایمیل بدیم.
    # این دیتیل=ترو هم که نوشتیم یعنی پی کی رو میخواد. پس تو یو آر ال یه عدد به عنوان پی کی
    # هم باید بهش بدیم.
    @action(detail=True, permission_classes=[SendPrivateEmailToCustomerPermission])
    def send_private_email(self, request, pk):
        return Response(f'Sending email to customer {pk=}')
    # این طوری به شرطی میتونه از این یو آر ال استفاده کنه که این پرمیشن رو داشته باشه یا ادمین باشه
    # http://127.0.0.1:8000/customers/10/send_private_email/
    # البته ادمین تمام پرمیشن ها رو داره. اما تابعی که جواب رو به ما میده دست خودمونه.
    # مثلا تو فایل پرمیشنز.پای، اون دو خط اول رو گذاشتم و دیدم که به کسی که ادمین هم باشه اجازه
    # دسترسی نمیده. حالا میشه شرط ها شو جا به جا کرد دیگه. صرفا جهت تست بود. وگرنه که درستش اینه
    # که ادمین به همه چی دسترسی داشته باشه.


class OrderViewSet(ModelViewSet):
    http_method_names = ['post', 'get', 'head', 'options', 'patch', 'delete'] # پوت رو نمیخوایم بدیم.
    # serializer_class=OrderSerializer # چون پیچیده تر میشه از متدش استفاده میکنیم به جای مقدار دادن به متغیر
    # queryset = Order.objects.all().select_related('customer').prefetch_related('items__product') # این کوئری خوب هست. اما پایینی
    # که تو متد گت کوئری ست نوشتیم خیلی خفن تره و روی همون هم اینر جوین میزنه و باز هم دستور بهینه
    # تری برای ارتباط با دیتابیس مینویسه. علاوه بر این که اگه چند لایه باشه باز هم بهینه تر هست
    # نسبت به این مدلی که بالا نوشتیم.
    # permission_classes = [IsAuthenticated] این هم چون میخوایم کاملتر بنویسیم تابعش رو اوراید میکنیم.
    # فقط دقت کنم که اسم تابعش گت پرمیشنز هست. نه گت پرمیشن کلسز. پس چون خود پرمیشن ها رو میخواد
    # و نه کلاس اونها رو، موقع ریترن کردن ازشون یک شیئ میسازیم یعنی همون پرانتز باز و بسته رو میذاریم
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        query_set = Order.objects.all().select_related('customer__user').prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product')
                )
            )
        user = self.request.user
        if user.is_staff:
            return query_set
        return query_set.filter(customer__user_id=user.id)
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return OrderCreateSerializer
        if self.request.method=='PATCH':
            return OrderUpdateSerializer
        if self.request.user.is_staff:
            return OrderForAdminSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    def create(self, request, *args, **kwargs):
        create_order_serializer = OrderCreateSerializer(data=request.data, context={'user_id': self.request.user.id})
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()
        serializer = OrderSerializer(created_order)
        return Response(serializer.data)
