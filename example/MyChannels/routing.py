"""
@software: PyCharm
@file: routing.py
@time: 2018/7/2 14:56
"""

from django.urls import path, include
from . import consumers

ws_urlpatterns = [
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer),
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer_channel),
    path('ws/chat/<slug:room_name>/', consumers.AsyncChatConsumer_channel),
]

chanNameRouter = {
    "send-noti": consumers.NotifyConsumer
}
