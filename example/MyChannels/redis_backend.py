"""
@software: PyCharm
@file: redis_backend.py
@time: 2018/7/3 15:42
"""
# channels settings
from channels_redis.core import RedisChannelLayer


class RedisChannel(RedisChannelLayer):
    # blpop_timeout=0
    pass
