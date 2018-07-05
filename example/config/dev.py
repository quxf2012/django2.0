"""
开发环境配置
"""
import os

# #限制import * 导入的属性,新加配置时加入该列表
# __all__ = ["SECRET_KEY", "DEBUG", "DATABASES", "CACHES"]

# 定位到manage.py文件所在的位置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'llo*3uru2ea1ovrz$^k9@_0-)pa*#4$&q=d$24c6i9)-l*&6j4'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database DB配置
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 缓存配置
CACHES = {
    'dummy': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'LOCATION': 'unique-snowflake',
    },
    'redis': {
        "BACKEND": "django_redis.cache.RedisCache",
        'TIMEOUT': 300,
        'LOCATION': [
            # '192.168.128.101:6379',
            '127.0.0.1:6379',
            # '<host>:<port>',
            # '<host>:<port>',
        ],
        'OPTIONS': {
            'DB': 1,
            # 'PASSWORD': 'yadayada',
            # 'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 100,
                'timeout': 20,
            },
            'PICKLE_VERSION': -1,
            # 'MASTER_CACHE': '<master host>:<master port>',
        },
    },
}
CACHES['default'] = CACHES['locmem']

"""
邮件配置
https://docs.djangoproject.com/en/2.0/topics/email/
"""
# EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# 模拟发邮件,邮件内容存入文件
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'mail.log')

"""
CSRF
https://docs.djangoproject.com/en/2.0/ref/settings/#security
https://docs.djangoproject.com/en/2.0/ref/csrf/#csrf-limitations
CSRF_COOKIE_DOMAIN=None

CSRF_TRUSTED_ORIGINS=["subdomain.example.com"]    #".example.com" all example.com subdomains
"""

"""
session配置
https://docs.djangoproject.com/en/2.0/ref/settings/#sessions
https://docs.djangoproject.com/en/2.0/topics/http/sessions/
SESSION_COOKIE_NAME='sessionid'
SESSION_COOKIE_PATH='/'
SESSION_COOKIE_SECURE=False

SESSION_EXPIRE_AT_BROWSER_CLOSE=False
    浏览器关闭后session过期,每次都需要重新登录.
SESSION_SAVE_EVERY_REQUEST=False

"""
# session入缓存并写一份到db中.
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = (60 * 60 * 24) * 14

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    "DOC_EXPANSION": "none"

}

REDOC_SETTINGS = {
    'LAZY_RENDERING': True,
}
