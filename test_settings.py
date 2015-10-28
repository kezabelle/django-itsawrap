from __future__ import absolute_import
import os
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'TESTTESTTESTTESTTESTTESTTESTTEST')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,testserver').split(',')
BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
SITE_ID = 1
ROOT_URLCONF = 'test_urls'
MIDDLEWARE_CLASSES = (
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.auth',
    'test_app',
)
STATIC_ROOT = os.path.join(BASE_DIR, 'test_collectstatic')
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'test_templates')]
TESTGUESS_ROOT = BASE_DIR
STATIC_URL = '/__static__/'
MEDIA_URL = '/__media__/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
