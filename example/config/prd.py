"""
生产环境配置
"""


# #限制import * 导入的属性
# __all__ = ["SECRET_KEY", "DEBUG", "DATABASES", "CACHES"]


"""
SECRET_KEY
https://docs.djangoproject.com/en/2.0/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
"""
SECRET_KEY = 'sjhd7a+_#jzs-j74_-9%b2$0+c=9=tdtlo9(wbexak4(!#rbg@'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


"""
Database DB配置
pip install mysqlclient>=1.3.12
https://docs.djangoproject.com/en/2.0/ref/settings/#databases
https://docs.djangoproject.com/en/2.0/ref/databases/#mysql-notes

AUTOCOMMIT=True
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'kBgFxf3b6',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # 'OPTIONS': {
        #     'read_default_file': '/path/to/my.cnf',
        # }

    }
}


"""
缓存配置
"""
CACHES = {
    'redis': {
        'BACKEND': 'redis_cache.RedisCache',
        'TIMEOUT': 300,
        'LOCATION': [
            '127.0.0.1:6379',
            # '<host>:<port>',
            # '<host>:<port>',
        ],
        'OPTIONS': {
            'DB': 1,
            # 'PASSWORD': 'yadayada',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
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
CACHES['default'] = CACHES['redis']


"""
邮件配置
https://docs.djangoproject.com/en/2.0/topics/email/
https://docs.djangoproject.com/en/2.0/ref/settings/#email-backend
"""
# EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = ""



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


