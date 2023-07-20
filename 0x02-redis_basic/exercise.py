#!/usr/bin/env python3
"""
This script contains a python class that helps in handling
operation as regards to Redis.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any


class Cache:
    """ The cache class that acts as a middle man. """

    def __init__(self):
        """
        This method creates an Instance of the redis class
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method takes a data argument, store it with a unique id
        and returns a string
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Callable) -> Any:
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
