from django import forms


# اول از این فرم استفاده کردیم و با کریسپی هم دیدیم. اما چون ظاهر اچ تی ام ال خودمون قشنگ تر بود،
# از همون استفاده کردیم. حالا چرا یان کد رو اینجا گذاشتیم، به خاطر این که داخل ویوز ازش استفاده
# کنیم و برای بررسی ولید بودن ازش استفاده کنیم. در واقع با این که تو اچ تی ام ال ازش استفاده نکردیم،
# اما اسم متغیرهای فرم اچ تی ام المون رو مثل این گذاشتیم و تو ویوز متغیرهای گرفته شده رو خود
# جنگو با این فرمی که اینجا ساختیم مقایسه میکنه. یعنی اگه کسی اچ تی ام ال رو دور بزنه و مثلا
# ۵۰ تا سفارش بده، خود جنگو هم حالا بهش گیر میده. اگه فرم تعریف نمیکردیم با کد پایتون خودمون
# باید دستی بررسیش میکردیم. اما حالا که فرم تعریف کردیم فقط تابع ایز ولید رو صدا کردیم.
class AddToCartProductForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)
    # این اتریبیوت اینپلیس رو برای این تعریف کردیم که بشه هم از تو خود محصول آیتم رو اضافه کرد
    # و هم از تو سبد خرید مقدار نهایی رو مشخص کرد. این دو تا فرق داره. اگه ۳ تا جوراب داشته باشیم
    # و بریم تو صفحه جوراب رو ۲ بزنیم باید ۲ تا به ۳ تای قبلی اضافه بشه و بشه ۵ تا.
    # اما اگه تو سبد خرید جوراب رو بزنیم ۳ تا یعنی میخوایم مقدار نهاییش ۳ تا باشه و جمع نمیشه.
    # به همین منظور این متغیر رو تعریف کردیم. اجباری نیست. چون تو صفحه خود جزییات محصول که میخوایم
    # اضافه کنیم نباید باشه. یعنی اونجا اینپلیس فالس هست. از طرفی خود کاربر هم نباید بفرسته. خودمون
    # میفرستیم با اچ تی ام ال. پس هیدن هم میذاریمش. تو صفحه سبد خرید هم همین طور. خود کاربر باهاش
    # کاری نداره. ما میذاریم که بدونیم توی اون صفحه هستیم و مقدار ترو اونجا بهش میدیم.
    
