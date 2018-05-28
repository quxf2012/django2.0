"""
https://docs.djangoproject.com/en/2.0/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
单独跑django脚本
BASE_DIR 和 manage.py所在目录
其他脚本中
from .base import *
"""
import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
