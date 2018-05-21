from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'example0518',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.128.101',
        'PORT': '3306',
    }
}

CACHES['redis']['LOCATION'] = [
    '192.168.128.101:6379',
    # '127.0.0.1:6379',
    # '<host>:<port>',
    # '<host>:<port>',
]

CACHES['default'] = CACHES['redis']
