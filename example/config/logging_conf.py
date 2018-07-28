"""
@software: PyCharm
@file: logging_conf.py
@time: 2018/7/27 16:06
"""
def getLogConf(loglevel="DEBUG", base_log_dir="/tmp", version=1, disable_existing_loggers=False):
    import os
    BASE_LOG_DIR = base_log_dir
    loglevel = loglevel
    LOGGING = {
        'version': version,
        'disable_existing_loggers': disable_existing_loggers,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s\t%(asctime)s\t%(name)s.%(funcName)s(%(lineno)d)\t%(message)s'
            },
            'simple': {
                'format': '%(levelname)s\t%(module)s[%(lineno)d]\t%(message)s'
            },
            'debug': {
                'format': '%(levelname)s\t%(asctime)s\t%(pathname)s.%(funcName)s(%(lineno)d)\t%(message)s'
            },
            'console': {
                'format': '%(levelname)s\t%(asctime)s\t%(name)s.%(funcName)s(%(lineno)d)\t%(message)s'
                # 'format': '%(levelname)s\t%(asctime)s\t%(message)s'
            }

        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                # 'filters':['special']
            },
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(BASE_LOG_DIR, 'cmdb.log'),
                'when': 'midnight'
            },
            'system': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(BASE_LOG_DIR, 'django.log')
            },

        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['system'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'MyChannels': {
                'handlers': ["default", 'console'],
                'level': loglevel
            },
            'utils': {
                'handlers': ["default", 'console'],
                'level': loglevel
            },
            'default': {
                'handlers': ["default", 'console'],
                'level': loglevel,
            },
            # 'django.request': {
            # 	'handlers': ['mail_admins'],
            # 	'level': 'ERROR',
            # 	'propagate': False,
            # },
            # 'manager': {
            #     'handlers': ['default'],
            #     'level': loglevel,
            #
            # },
            # 'workflow': {
            #     'handlers': ['default'],
            #     'level': loglevel,
            # },

        }
    }

    return LOGGING


DEFAULT_LOGGING = getLogConf()
