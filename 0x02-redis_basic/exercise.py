#!/usr/bin/env python3
"""
This script contains a python class that helps in handling
operation as regards to Redis.
"""
import redis
from uuid import uuid4
from typing import Union


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
