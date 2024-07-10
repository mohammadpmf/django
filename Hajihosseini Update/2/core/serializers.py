from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer



# برای این که از این سریالایزرها استفاده کنه، داخل فایل ستینگز.پای باید متغیر زیر رو تعریف کنیم
# DJOSER
# و به اون صورتی که اونجا نوشتم ازش استفاده میشه.

# تعریف این سریالایزر، به خاطر اینه که بگیم موقع ثبت نام چه فیلدهایی از یوزر رو نشون بده و فقط
# یوزرنیم و پسورد نباشه. مثلا اگه خواست اسمش رو هم عوض بکنه، بتونه همونجا بذاره. در واقع یو آر ال
# /auth/users
# رو داریم بهش میگیم که موقع نشون دادنش چه چیزی هایی رو به ما نشون بده و اجازه پست کردنشون
# رو داشته باشیم و این که بعد از ساخته شدن، اطلاعاتی رو که به ما نشون میده همینا هستند.
# در واقع serializer.data ای رو که درست کرده رو به ما میده.
class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']



# تعریف این سریالایزر به خاطر اینه که بگیم داخل صفحه
# /auth/users/me
# چه چیزهایی رو به ما نشون بده
# پسورد رو به صورت هش شده نشون میده البته که به درد نمیخوره. ولی گذاشتم باشه.
# لیست خالی هم گذاشتم هیچ چیزی نشون نداد😁 خلاصه این که مربوط میشه به نمایش اطلاعات
# در صفحه ای که گفتم
class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']


# این هم آخر سر خودم ور روفتم باهاش. وقتی اکسکلود گذاشتم گفت که نمیشه هم فیلدز بنویسی هم اکسکلود
# به خاطر این که تو حالت قبلی کلاس متا هم ارث بری کرده بود که اونجا فیلدز رو خودش نوشته بود.
# اگه ارث بری نکنیم این شکلی از اکسکلود استفاده کردم که خب وقتی طرف میرفت تو جزییات صفحه خودش،
# میتونست گروه های خودش رو عوض کنه یا حتی خودش رو سوپریوزر و استف بکنه که به همه چی دسترسی
# داشته باشه. کلا جهت کنجکاوی بررسیش کردم اما لازم نیست که اون ها رو بذاریم و اضافه هست. همین
# مدل بالایی که نوشتم کافی و درست هست.
# from django.contrib.auth import get_user_model
# User = get_user_model()
# class UserSerializer(DjoserUserSerializer):
#     class Meta:
#         model = get_user_model()
#         exclude =['id']
