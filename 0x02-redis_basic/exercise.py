#!/usr/bin/env python3
"""
Storing data with Redis
"""

import uuid
from typing import Union
import redis


class Cache:
    """
    A class that stores an instance of the redis client
    """
    def __init__(self):
        """
        A class contructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        A class method that stores an instance of the redis client
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
