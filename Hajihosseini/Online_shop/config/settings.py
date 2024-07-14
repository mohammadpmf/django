"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from environs import Env

# برای تعریف متغیرهای محیطی که برای امنیت کلید و این ها استفاده میشه.
env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
# مقداری که اینجا بود رو به اون صورت داخل فایل docker-compose.yml می نویسیم و دقت کنم که
# علامت $ هر جا بود باید یه $ دیگه کنارش بنویسیم. چون برای داکر کامپوز اسکیپ کاراکتر هست.


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG")

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.herokuapp.com']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',


    # Local apps
    'accounts',
    'pages',
    'products.apps.ProductsConfig', # این بار این مدلی کانفیگ کردم که هر دو مدل رو دیده باشیم
    # داخل اپ، داخل فایل اپز.پای یه کلاس میسازه به اسم اپمون با یه کانفیگ تهش که میشه این
    # مدلی هم داخل استرینگ نوشت. نوشتم یه نمونه داشته باشم فقط
]

SITE_ID = 1 # حاجی حسینی گذاشته بود. اما تو لینکه نبود. گذاشتم اوکی بود دیگه حذفش نکردم.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########################     EMAIL     ########################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_SSL = True
# EMAIL_PORT = 465 # SSL
# However, SSL is an older technology that contains some security flaws.
# Transport Layer Security (TLS) is the upgraded version of SSL that fixes existing SSL vulnerabilities.
# TLS authenticates more efficiently and continues to support encrypted communication channels.
# خلاصه این که اس اس ال یه مشکلاتی داشت و ورژن تی ال اس رو دادن که امن تره
EMAIL_USE_TLS = True
EMAIL_PORT = 587 # TLS
EMAIL_HOST_USER = env('MY_EMAIL_ADDRESS')
EMAIL_HOST_PASSWORD = env('MY_APP_PASSWORD')
########################     END EMAIL     ########################


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# accounts config
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# crispy form config
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'


# all auth config البته خیلی هاش وسط کدها بود. این تیکه رو جدا نوشتم
# ACCOUNT_SESSION_REMEMBER = True # تیک ریممبر می رو به صورت پیش فرض فعال میذاره و دیگه به کاربر هم نشون نمیده.
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False # به صورت پیش فرض ترو هست و ۲ بار میپرسه. اگه فالسش کنیم یه بار میپرسه موقع ثبت نام
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ATHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
