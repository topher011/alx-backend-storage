#!/usr/bin/env python3
'''
A Cache class that interfaces with redis
'''
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def replay(mthd: Callable) -> None:
    '''
    a replay function to display the history of calls of a particular function
    '''
    method_key = mthd.__qualname__
    key_inputs = method_key + ":inputs"
    key_outputs = method_key + ":outputs"
    redis = mthd.__self__._redis
    count = redis.get(method_key).decode("utf-8")
    print("{} was called {} times:".format(method_key, count))
    ListInput = redis.lrange(key_inputs, 0, -1)
    ListOutput = redis.lrange(key_outputs, 0, -1)
    allData = list(zip(ListInput, ListOutput))
    for key, data in allData:
        attr, data = key.decode("utf-8"), data.decode("utf-8")
        print("{}(*{}) -> {}".format(method_key, attr, data))


def call_history(method: Callable) -> Callable:
    '''
    Records the history of a wrapped function inputs
    '''
    list_in = "{}:inputs".format(method.__qualname__)
    list_out = "{}:outputs".format(method.__qualname__)

    @wraps(method)
    def wrapped(self, *args, **kwargs) -> str:
        '''
        decorated function
        '''
        self._redis.rpush(list_in, str(args))
        response = method(self, *args, **kwargs)
        self._redis.rpush(list_out, str(response))
        return response
    return wrapped


def count_calls(method: Callable) -> Callable:
    '''
    wraps decorated function and stores the number
    of time method has been stored
    '''
    key = method.__qualname__

    @wraps(method)
    def wrapped(self, *args, **kwargs) -> str:
        '''
        decorated function
        '''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapped


class Cache:
    '''
    Interface class for redis
    '''
    def __init__(self) -> None:
        '''
        class construction
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        takes a data argument and returns a string
        '''
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str,
            fn: Union[Callable, None] = None) -> Union[int, str, float]:
        '''
        Ensures get format is correct
        '''
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        '''
        Ensures get format is correct for strings
        '''
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        '''
        Ensures get format is correct for integers
        '''
        return self.get(key, int)
