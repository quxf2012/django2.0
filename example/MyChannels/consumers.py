"""
@software: PyCharm
@file: consumers.py
@time: 2018/7/2 17:35
"""

import asyncio
import json
# from channels.security.websocket import AllowedHostsOriginValidator
import logging
import threading
import paramiko
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import time
import datetime
import socket

socket.setdefaulttimeout(5)

logger = logging.getLogger(__name__)


def logthread(key):
    logger.debug(f'{key}  {threading.current_thread()}')


def datetime1():
    return datetime.datetime.now()


def sshClient():
    try:
        # logger.debug(f'sshClient {threading.current_thread()}')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.debug(f"connect start {datetime1()}")
        # time.sleep(1000)
        ssh_client.connect('127.0.0.1', 22, 'quxf', '1111')
        logger.debug(f"connect end {datetime1()}")
        # std_in, std_out, std_err = ssh_client.exec_command(command)
        # shell = ssh_client.invoke_shell(term="xterm")  # width=200, height=300
        # shell.recv()
        return ssh_client
    except Exception as e:
        logger.debug(f"error end {datetime1()}")
        logger.error(e)


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

        # send(msg)

    # @staticmethod
    # def sed_shell_to_client_with_executor(shell,send):

    def shell_recv(self):
        # time.sleep(10)
        # logthread('shell_recv')
        data = self.shell.recv(65535)
        # time.sleep(10)
        return data

    def run_in_executor(self, call, *args):
        """ run in default execuror"""
        return self.loop.run_in_executor(None, call, *args)

    async def _from_shell_get_data(self, use_executor=True):
        # time.sleep(3)
        # time.sleep(10)

        # logger.debug(f'reader {threading.current_thread()}')
        # 从不支持协程的函数中取数

        if not self.shell.recv_ready():
            return
        self.remove_reader()
        # msg = self.shell_recv()

        # msg = await self.run_in_executor(self.shell.recv,65535)
        # logger.debug("recv data start ..")
        msg = await self.run_in_executor(self.shell_recv)
        # logger.debug("recv data end ..")

        # logger.debug(f'reader end {threading.current_thread()}')

        # if use_executor:
        #     """在另一个线程里面执行回调函数"""
        #     self.run_in_executor(async_to_sync(self.async_send), msg)
        #     # asyncio.run(self.async_send(msg)) #不能在一个loop中
        # else:
        # """在默认循环中执行回调函数 create_task(首选) 和 ensure_future都可以"""
        await self.async_send(msg)
        self.add_reader(use_executor)
        # asyncio.ensure_future(send)
        # logger.debug(send)

    def from_shell_get_data(self, use_executor=True):
        self.loop.create_task(self._from_shell_get_data(use_executor))

    def _disconnect_ssh(self):
        self.shell.close()
        self.remove_reader()
        logger.debug("Connect closed!")
        self.ssh.close()

    async def disconnect(self, code):
        await self.async_send("连接已关闭..")
        self.run_in_executor(self._disconnect_ssh)


    def add_reader(self, use_executor):
        self.loop.add_reader(self.shell_fd, self.from_shell_get_data, use_executor)

    def remove_reader(self):
        self.loop.remove_reader(self.shell_fd)

    async def set_shell(self, use_executor=True):
        # time.sleep(10)
        # time.sleep(10)
        # logger.debug(f'set_shell {threading.current_thread()}')
        self.ssh = await self.run_in_executor(sshClient)
        self.shell = self.ssh.invoke_shell(term="xterm")
        # self.shell.settimeout(0)
        self.shell_fd = self.shell.fileno()
        # self.shell.
        self.add_reader(use_executor)

    # def set_shell1(self):
    #     self.ssh = sshClient()
    #     self.shell = self.ssh.invoke_shell(term="xterm")
    #     self.shell.settimeout(0)
    #     self.shell_fd = self.shell.fileno()
    #     self.loop.add_reader(self.shell_fd, self.from_shell_get_data, self.shell, async_to_sync(self.async_send))

    async def connect(self):
        self.loop = asyncio.get_event_loop()
        # self.new_loop = asyncio.new_event_loop()
        # logger.debug(f'connect {threading.current_thread()}')
        await self.accept()
        await self.async_send("Hello\r\n")
        await self.set_shell()

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
