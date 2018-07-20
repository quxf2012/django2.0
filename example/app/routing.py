"""
@software: PyCharm
@file: routing.py
@time: 2018/7/2 14:56
"""

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import MyChannels.routing
from channels.sessions import SessionMiddlewareStack

import logging

logger = logging.getLogger("log")

# 根据请求协议来路由
application = ProtocolTypeRouter(

    {
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    MyChannels.routing.ws_urlpatterns
                )
            )
        ),
        'channel': ChannelNameRouter(
            MyChannels.routing.BackgroundTaskRouter
        )
    }
)
