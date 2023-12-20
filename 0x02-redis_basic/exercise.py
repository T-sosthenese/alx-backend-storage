#!/usr/bin/env python3
"""
Storing data with Redis
"""

import uuid
import redis
from typing import Callable, Union, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that takes a function fn as an argument. It defines a new
    function wrapper that increments a counter in Redis every time the
    method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A function that increments the counter every time a method is
        called.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Counts the number of instances a function has been called.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function.
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


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
    @call_history
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
