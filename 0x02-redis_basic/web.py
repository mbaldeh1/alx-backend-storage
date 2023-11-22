#!/usr/bin/env python3
"""Advanced task for Redis"""
import redis


def get_page(url: str) -> str:
    """get_page"""
    key = f"count:{url}"
    red = redis.Redis()
    red.incr(key)
    return red.get(url)


def get_status(status: int) -> str:
    """get_status"""
    key = f"status:{status}"
    red = redis.Redis()
    red.incr(key)
    return red.get(status)


def get_stats() -> str:
    """get_stats"""
    red = redis.Redis()
    keys = red.keys("status:*")
    keys.sort()
    total = 0
    stats = []
    for key in keys:
        status = key.decode("utf-8").split(":")[1]
        count = red.get(key).decode("utf-8")
        total += int(count)
        stats.append(f"{status}: {count}")
    stats.append(f"total: {total}")
    return "\n".join(stats)
