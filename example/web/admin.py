from django.contrib import admin

# Register your models here.
from .models import Assets


#在admin中注册绑定
# admin.site.register(Blog, BlogAdmin)
admin.site.register(Assets)
