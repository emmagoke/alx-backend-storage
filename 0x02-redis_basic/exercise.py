#!/usr/bin/env python3
"""
This script contains a python class that helps in handling
operation as regards to Redis.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    This decorator tracks the number of calls made by method in the cache
    (takes a single method Callable argument and returns a Callable)
    """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        This function  increments the count for that key every time the class
        method is called and returns the value returned by the original method.
        e.g
        cache.store(b"first")
        print(cache.get(cache.store.__qualname__))
        >> 1
        """

        # if isinstance(self._redis, redis.Redis):
        #  calling the decorated method
        self._redis.incr(key)

        #  returning the decorated function
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Append input and output when a function is called. """
    _key = method.__qualname__
    _input_list = _key + ":inputs"
    _output_list = _key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kargs):
        """ The function append the input and output of the decorated
         to the end of the list."""
        self._redis.lpush(_input_list, str(args))
        result = method(self, *args, *kargs)
        self._redis.lpush(_output_list, result)

        return result
    return wrapper


def replay(func: Callable) -> None:
    """
    This function display the history of calls of a particular function.
    """
    if func is None or not hasattr(func, '__self__'):
        return
    _redis = getattr(func.__self__, '_redis', None)

    count = int(_redis.get(func.__qualname__))
    input_list = _redis.lrange(func.__qualname__ + ':inputs', 0, -1)
    output_list = _redis.lrange(func.__qualname__ + ':outputs', 0, -1)
    output = ""
    method_name = func.__qualname__

    print("{} was called {} times:".format(method_name, count))
    for key, value in zip(input_list, output_list):
        print("{}(*{}) -> {}".format(method_name, key.decode('utf-8'), value))


class Cache:
    """ The cache class that acts as a middle man. """

    def __init__(self):
        """
        This method creates an Instance of the redis class
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method takes a data argument, store it with a unique id
        and returns a string
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(
            self,
            key: str,
            fn: Callable = None
            ) -> Any:  # or Union[str, bytes, int, float]
        """
        This method take a key string argument and an optional Callable
        This callable will be used to convert the data back to
        the desired format.
        """

        value = self._redis.get(key)
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key: str) -> str:
        """
        This method return a return a utf-8 decode value of
        self.get
        """

        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        This method return a integer fashion of the value
        self.get returns
        """

        return self.get(key, int)
