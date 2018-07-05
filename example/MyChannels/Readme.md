# channels

## 安装
    pip install channels
## 新建app
    python3 manage.py startapp MyChannels
    
## 创建根routing文件,类似于django的根urls
``` python
#app/routing.py
from channels.routing import ProtocolTypeRouter
application = ProtocolTypeRouter(
    {

    }
)
```


## 启用
    INSTALLED_APP+=["channels","MyChannels"]
    #设置websocket的根路由文件
    ASGI_APPLICATION = 'app.routing.application'

## 建立消费文件
``` python
# MyChannels/consumers.py
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, \
AsyncJsonWebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = text_data
        if bytes_data:
            data = bytes_data.decoce()

        message = json.loads(data)["message"]

        self.send(text_data=json.dumps({'message': "from Server:" + message}))
```

## 建立路由文件
``` python
#MyChannels/routing.py
from django.urls import path, include
from . import consumers

ws_urlpatterns = [
    path('ws/chat/<slug:room_name>/', consumers.ChatConsumer),
]


```

## 加入URLRouter中
``` python
#app/routing.py
from channels.routing import ProtocolTypeRouter
application = ProtocolTypeRouter(

    {
        'websocket': AuthMiddlewareStack(
            URLRouter(
                MyChannels.routing.ws_urlpatterns
            )
        )
    }
)

```


# channels channel layer
* 通道(channel)层是一个通信系统,允许多个consumer之间互相通信,或者其他django的其他模块
* 一个通道是一个消息队列,每个通道都有名字,任何拥知道该通道名称的人可以向该通道发送消息
* [group](https://channels.readthedocs.io/en/latest/tutorial/part_2.html#enable-a-channel-layer)通道组,可以向组中新建和删除通道,
可以通过组发送消息给所有组内的通道.
* 每个消费者(consumer)有一个随机生成的唯一名称


## 安装依赖
### 使用通道组需要redis的支持
`pip install channels_redis`
### 添加配置
``` python
#app/setting.py
ASGI_APPLICATION = 'app.routing.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379), ]
        }
    }
}
```

## 通道组
聊天室的例子,向通道组发消息,所有组内的成员都可以收到信息

### 改造消费文件向组发送消
``` python
class ChatConsumer_channel(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 加入group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        self.send_group(f"Server: {self.channel_name}加入了.")

    def send_group(self, message, type='chat_message'):
        # 向组发送消息
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": type,  # 消息类型
                "message": message
            }
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        data = text_data
        if bytes_data:
            data = bytes_data.decoce()

        message = json.loads(data)["message"]

        # 向组发送消息
        # self.send_group(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",  # 消息类型
                "message": f"{self.channel_name}说: {message}"
            }
        )

    def chat_message(self, event):
        "type: chat_message"
        message = event["message"]
        self.send(text_data=json.dumps({'message':  message}))


```

### 改造路由文件
``` python
#MyChannels/routing.py
from django.urls import path, include
from . import consumers

ws_urlpatterns = [
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer),
    path('ws/chat/<slug:room_name>/', consumers.ChatConsumer_channel),
]

```

### 打开两个窗口发送消息
两个窗口消息互通

### ChatConsumer_channel
#### self.scope[‘url_route’][‘kwargs’][‘room_name’]
每个consumer都有scope,包含当前连接信息,URL中的位置参数和命名参数,当前用户的认证信息

#### async_to_sync(self.channel_layer.group_add)(…)
self.channel_layer.group_add 加入通道组
WebsocketConsumer是同步调用但是所有的通道层方法是异步的,所以需要使用async_to_sync转换一下

#### self.accept()
接受websocket连接,如果不调用连接会被关闭

#### async_to_sync(self.channel_layer.group_send)
发送一个事件到group中
type: 事件的类型,目标consumer中的同名方法会被调用


## 聊天室,consumer异步化
await 只能用于awaitable对象
``` python
class AsyncChatConsumer_channel(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 加入group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_group(f"Server: {self.channel_name}加入了.")

    async def send_group(self, message, type='chat_message'):
        # 向组发送消息
        await  self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": type,  # 消息类型
                "message": message
            }
        )

    async def disconnect(self, code):
        await  self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = text_data
        if bytes_data:
            data = bytes_data.decoce()

        message = json.loads(data)["message"]

        # 向组发送消息
        # self.send_group(message)
        await  self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # 消息类型
                "message": f"{self.channel_name}说: {message}"
            }
        )

    async def chat_message(self, event):
        "type: chat_message"
        message = event["message"]
        await self.send(text_data=json.dumps({'message': message}))



#MyChannels/routing.py
ws_urlpatterns = [
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer),
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumer_channel),
    path('ws/chat/<slug:room_name>/', consumers.AsyncChatConsumer_channel),
]        
```
