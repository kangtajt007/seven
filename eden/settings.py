import os,mimetypes

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '@s)czz$9t1&13me^!xtmkune#2-81!9g7*ylj_yh3!u=4(#6fy'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum',
    'utente',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eden.urls'

WSGI_APPLICATION = 'eden.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dudu',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'http://bcs.duapp.com/dudufile/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__),'../static/').replace("\\",'/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.163.com'
EMAIL_PORT= 25
EMAIL_HOST_USER = 'kangtajt007'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

mimetypes.add_type("audio/mpeg",".mp3",True)

APPEND_SLASH=False

LOGIN_URL='/utente/login/'