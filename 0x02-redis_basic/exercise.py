#!/usr/bin/env python3
"""
Storing data with Redis
"""

import uuid
from typing import Union
import redis
from typing import Callable
from functools import wraps


def count_calls(fn):
    """
    A decorator that takes a function fn as an argument. It defines a new
    function wrapper that increments a counter in Redis every time the
    method is called.
    """
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        """
        A function that increments the counter every time a method is
        called.
        """
        key = fn.__qualname__
        self._redis.incr(key, amount=1)
        return fn(self, *args, **kwargs)
    return wrapper


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

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        A class method that stores an instance of the redis client
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None
    ) -> Union[str, bytes, int, float]:
        """
        A method that takes any key string argument and an optional callable
        function fn. The callable is used to convert data back to the desired
        format. It conserves the original Redis.get behavior if the key does
        not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        This method retrieves data associated with a given key from Redis
        and decodes it from bytes to a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves data and converts it to an integer
        """
        return self.get(key, fn=int)
