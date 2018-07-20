"""
@software: PyCharm
@file: routing.py
@time: 2018/7/2 14:56
"""

from django.urls import path

from . import BackgroundTask
from . import consumers

ws_urlpatterns = [
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer),
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer_channel),
    path('ws/chat/<slug:room_name>/', consumers.AsyncChatConsumer_channel),
    path('ws/webshell/', consumers.WebShellConsumer),
]

BackgroundTaskRouter = {
    "NotifyTask": BackgroundTask.NotifyTaskConsumer,
    "AsyncTask": BackgroundTask.AsyncTaskConsumer,
}

# channel_layer.send(
#             "NotifyTask", {
#                 "type": "message.noti", ->BackgroundTask.NotifyTaskConsumer.message_noti
#                 "message": "Hello"
#             }
# )
#
# channel_layer.send(
#             "AsyncTask", {
#                 "type": "echo.back",  #->BackgroundTask.AsyncTaskConsumer.echo_back
#                 "message": "Hello",
#                 "id":"2"
#             }
# )
