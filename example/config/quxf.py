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
