"""
@software: PyCharm
@file: urls.py
@time: 2018/7/2 18:13
"""

from django.urls import path

from . import views

urlpatterns = [
    path("room/<slug:room_name>/", views.room, name="room")

]
