"""
@software: PyCharm
@file: consumers.py
@time: 2018/7/2 17:35
"""

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, \
    AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from asgiref.sync import async_to_sync
# from channels.security.websocket import AllowedHostsOriginValidator
import logging
import time

logger = logging.getLogger('log')

from asyncio import AbstractEventLoop
class NotifyConsumer(AsyncConsumer):

    async def message_noti(self, message):
        time.sleep(10)
        logger.debug(message)


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


class ChatConsumer_channel(WebsocketConsumer):
    # groups=None
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
        self.send(text_data=json.dumps({'message': message}))


class AsyncChatConsumer_channel(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("Connect...")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 加入group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.group_send(f"Server: {self.channel_name}加入了.")

    async def group_send(self, message, type='chat_message'):
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
        await  self.group_send(f"Server: {self.channel_name}离开了.")

    async def receive(self, text_data=None, bytes_data=None):
        data = text_data
        if bytes_data:
            data = bytes_data.decoce()

        message = json.loads(data)["message"]

        # 向组发送消息
        # self.send_group(message)
        logger.debug("发送事件")
        # todo 发送自定义的事件
        await self.channel_layer.send(
            "send-noti", {
                "type": "message.noti",
                "message": "Hello"
            }
        )
        await  self.group_send(f"{self.channel_name}说: {message}")
        # await  self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         "type": "chat.message",  # 消息类型
        #         "message": f"{self.channel_name}说: {message}"
        #     }
        # )

    async def chat_message(self, event):
        "type: chat_message"
        logger.debug(event)
        message = event["message"]
        await self.send(text_data=json.dumps({'message': message}))
