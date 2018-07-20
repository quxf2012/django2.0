"""
@software: PyCharm
@file: BackgroundTask.py
@time: 2018/7/5 17:14
"""

import logging

from channels.consumer import AsyncConsumer

logger = logging.getLogger('log')


class NotifyTaskConsumer(AsyncConsumer):

    async def message_noti(self, message):
        logger.debug(message)


class AsyncTaskConsumer(AsyncConsumer):

    async def echo_back(self, message):
        logger.debug(message)
