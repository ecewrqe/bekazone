import os
from bekazone import utils
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fqcbjs4t#%)-m*)$igcr_mo4f)47(^d*c(+-vy)o@(7c7=iq#b'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'cadmin',

    'blog_backend',
    'framework_test',
    'rest_framework',
]


CONFIGFILE_PATH = "etc/bekazone/config.conf"
kcp = utils.BekaConfigParser(os.path.join(BASE_DIR, CONFIGFILE_PATH))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'bekazone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'bekazone.wsgi.application'


# database configuration
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': kcp.get_mysql_config("name"),
       'USER': kcp.get_mysql_config("user"),
       'PASSWORD': kcp.get_mysql_config("password"),
       'HOST': kcp.get_mysql_config("host"),
       'PORT': kcp.get_mysql_config("port"),
   }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
# anti-interational
USE_TZ = False


STATIC_URL = '/static/'
# my staticfiles in write in static folder
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'blog_backend/static'),
    os.path.join(BASE_DIR, 'var/data'),

]
# a thrill of my wife pregnented

# expired
USER_SESSION_EXPIRED = kcp.get_config("bekazone", "user_session_expired")
if USER_SESSION_EXPIRED:
    USER_SESSION_EXPIRED = eval(USER_SESSION_EXPIRED)

# framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}