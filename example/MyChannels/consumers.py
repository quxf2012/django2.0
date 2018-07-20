"""
@software: PyCharm
@file: consumers.py
@time: 2018/7/2 17:35
"""

import asyncio
import json
# from channels.security.websocket import AllowedHostsOriginValidator
import logging

import paramiko
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger('log')


def sshClient():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect('127.0.0.1', 22, 'quxf', '1111')
        # std_in, std_out, std_err = ssh_client.exec_command(command)
        # shell = ssh_client.invoke_shell(term="xterm")  # width=200, height=300
        # shell.recv()
        return ssh_client
    except Exception as e:
        print(e)


# AsyncJsonWebsocketConsumer
class WebShellConsumer(AsyncWebsocketConsumer):
    loop = None
    shell = None
    ssh = None
    shell_fd = 0

    async def async_send(self, message):
        if isinstance(message, bytes):
            message = message.decode(errors="ignore")
            # logger.debug(message)
        data = json.dumps(['stdout', message])
        # await self.send(bytes_data=json.dumps(['stdout', message]).encode())
        await self.send(data)

    def from_shell_get_data(self):

        msg = self.shell.recv(65535)
        # logger.debug(f"callback{msg}")
        loop = asyncio.get_event_loop()
        send = self.async_send(msg)
        loop.create_task(send)
        # logger.debug(send)

    def _disconnect_ssh(self):

        self.shell.close()
        self.loop.remove_reader(self.shell_fd)
        self.ssh.close()

    async def disconnect(self, code):
        sync_to_async(self._disconnect_ssh)()

    def set_shell(self):
        self.ssh = sshClient()
        self.shell = self.ssh.invoke_shell(term="xterm")
        self.shell.settimeout(0)
        self.shell_fd = self.shell.fileno()
        self.loop.add_reader(self.shell_fd, self.from_shell_get_data)

    async def connect(self):
        self.loop = asyncio.get_event_loop()

        await self.accept()
        self.set_shell()
        # logger.debug(self.ssh)
        # logger.debug(self.shell)

    # async def disconnect(self, code):
    #     await  self.group_send(f"Server: {self.channel_name}离开了.")

    async def receive(self, text_data=None, bytes_data=None):
        # data = text_data
        # if bytes_data:
        #     data = bytes_data.decoce()
        # logger.debug(data)
        command = json.loads(text_data)
        msg_type = command[0]

        if msg_type == "stdin":
            message = command[1]
            await sync_to_async(self.shell.send)(message)
        elif msg_type == "set_size":
            size = command[1:3]
            self.shell.resize_pty(*size)
            await self.async_send("窗口改变")
            # self.terminal.resize_to_smallest()
        # elif msg_type == "set_size":
        #     self.size = command[1:3]
        #     self.terminal.resize_to_smallest()

        # await  self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         "type": "chat.message",  # 消息类型
        #         "message": f"{self.channel_name}说: {message}"
        #     }
        # )


# AsyncJsonWebsocketConsumer
class AsyncChatConsumer_channel(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("Connect...")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.user_name=self.scope
        self.room_group_name = f'chat_{self.room_name}'

        # 加入group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.group_send(f"Server: {self.channel_name}加入了.")

    async def group_send(self, message, type='chat.message'):
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
            "NotifyTask", {
                "type": "message.noti",
                "msg": message,
                "group_name": self.room_group_name
            }
        )

        await self.channel_layer.send(
            "AsyncTask", {
                "type": "echo.back",
                "msg": message,
                "group_name": self.room_group_name
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

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, code):
#         pass
#
#     def receive(self, text_data=None, bytes_data=None):
#         data = text_data
#         if bytes_data:
#             data = bytes_data.decoce()
#
#         message = json.loads(data)["message"]
#
#         self.send(text_data=json.dumps({'message': "from Server:" + message}))
#
#
# class ChatConsumer_channel(WebsocketConsumer):
#     # groups=None
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         # 加入group
#         async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
#         self.accept()
#         self.send_group(f"Server: {self.channel_name}加入了.")
#
#     def send_group(self, message, type='chat.message'):
#         # 向组发送消息
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 "type": type,  # 消息类型
#                 "message": message
#             }
#         )
#
#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
#
#     def receive(self, text_data=None, bytes_data=None):
#         data = text_data
#         if bytes_data:
#             data = bytes_data.decoce()
#
#         message = json.loads(data)["message"]
#
#         # 向组发送消息
#         # self.send_group(message)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 "type": "chat.message",  # 消息类型
#                 "message": f"{self.channel_name}说: {message}"
#             }
#         )
#
#     def chat_message(self, event):
#         "type: chat_message"
#         message = event["message"]
#         self.send(text_data=json.dumps({'message': message}))
