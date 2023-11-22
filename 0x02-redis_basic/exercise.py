#!/usr/bin/env python3
"""Exercise for Redis"""
from typing import Union, Callable, Optional
from functools import wraps
import uuid
import redis


# task 2
def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper
# end of task 2


# task 3
def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        inputt = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", inputt)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper
# end of task 3


class Cache:
    """Cache class"""
    # task 0
    def __init__(self):
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history  # task 3
    @count_calls  # task 2
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key, store the input data in Redis using the key
        and return the key"""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key
    # end of task 0

    # task 1
    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """take a key string argument and an optional Callable argument named
        fn. This callable will be used to convert the data back to the desired
        format"""
        if fn:
            return fn(self._redis.get(key))
        else:
            return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get to str"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get to int"""
        return self.get(key, int)
    # end of task 1


# task 4
def replay(method: Callable):
    """display the history of calls of a particular function"""
    red = redis.Redis()
    method_name = method.__qualname__
    count = red.get(method_name).decode('utf-8')
    inputs = red.lrange(method_name + ":inputs", 0, -1)
    outputs = red.lrange(method_name + ":outputs", 0, -1)

    print(f"{method_name} was called {count} times:")

    for inp, out in zip(inputs, outputs):
        print(
            f"{method_name}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}"
        )
# end of task 4
