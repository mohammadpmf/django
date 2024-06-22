from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AccountsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_user(username='admin', password='admin')

    def test_get_home_page_by_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_home_page_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_does_home_page_show_word_khaneh(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'خانه')

    def test_is_home_page_html_file_name_homedothtml(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_get_signup_page_by_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_get_signup_page_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_does_signup_page_show_word_sabte_nam(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'ثبت نام')

    def test_is_signup_page_html_file_in_registration_folder_and_its_name_is_signupdothtml(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')
    
    def test_does_signup_form_work(self):
        # آخرین نکته که از نیم ساعت ور روفتن با تابع create_user متوجه شدم رو اینجا مینویسم که این 
        # دفعه دیگه نیم ساعت باهاش ور نرم. ورودی هاش این شکلی ان
        # یوزرنیم، ایمیل و پسورد
        # ترتیبشون به همین صورته و اگه بخوایم بدون نام ازش استفاده کنیم نوشتم که یادم باشه
        # اگه بخوایم با نام صدا کنیم که میشه ترتیب رو عوض کرد و مسئله ای نیست.
        # ورودی یوزرنیم اجباریه. بقیه اختیاری. یعنی میشه ایمیل و پسورد نداد.
        # بقیه ورودی ها رو میتونیم با نام بهش بدیم
        self.user = get_user_model().objects.create_user(
            username='new user',
            email='test@gmail.com',
            password='new password',
            gender='m',
            )
        self.assertEqual(get_user_model().objects.last().username, self.user.username)
        self.assertEqual(get_user_model().objects.last().password, self.user.password)
        self.assertEqual(get_user_model().objects.last().email, self.user.email)
        self.assertEqual(get_user_model().objects.last().gender, self.user.gender)
        self.assertEqual(get_user_model().objects.last().nat_code, self.user.nat_code)
        self.assertEqual(get_user_model().objects.last().phone_number, self.user.phone_number)
        self.assertEqual(get_user_model().objects.last().first_name, self.user.first_name)
        self.assertEqual(get_user_model().objects.last().last_name, self.user.last_name)
        self.assertEqual(get_user_model().objects.last().last_login, self.user.last_login)
        # دقت کنم چیزایی هم که اختیاری بودن موقع ساخت بهش ندادم، خب من ندادم. اما با هم برابر هستند
        # الکی فقط چک کردم که ببینم داره یا نه که دیدم داره. اما چیزی مثل avcrtb که اصلا تو کلاس
        # نبود رو وقتی مینویسم بهم ارور میده. یعنی خط بعدی رو از کامنت در بیارم ارور میده
        # self.assertEqual(get_user_model().objects.last().avcrtb, self.user.avcrtb)
        # نکته آخر این که موقع ساخت، تابع create_user فقط username رو از ما میخواد
        # یعنی اگه بهش پسورد هم ندیم میسازه باز. اما بدون ورودی ارور میداد. بعضی از چیزهایی که
        # تو کلاس کاستوم یوزر بودند رو تستی بهش دادم که ببینم درست کار میکنه که دیدم درسته.
        # اما جنسیت و امیل اینا اختیاری بودند که ندیم هم مشکلی نیست. یه تابع create داره که میشه
        # بهش ورودی هم نداد و معلوم نیست به چه دردی میخوره اصلا :دی پسورد رو هم هش نمیکنه.
        # اما create_user پسورد رو هش میکنه و حداقل یوزرنیم رو میگه وارد کنید. خلاصه
        # آخر سر بگم که لازم نیست این همه چیز رو چک کنم برای این تست (یعنی این تابع خاص)
        # اسم تابع اینه که ببینیم ساین آپ فرم کار میکنه یا نه. پس خود آبجکت ساخته شده رو میتونیم
        # مقایسه بکنیم ببینیم خودش هست یا نه یعنی همه اسرت های قبلی رو کامنت کنم و این رو بنویسم.
        # self.assertEqual(get_user_model().objects.last(), self.user)
        # یا مثلا تعداد یوزرها رو بشمارم ببینم ساخته
        # self.assertEqual(get_user_model().objects.all().count(), 2)
        