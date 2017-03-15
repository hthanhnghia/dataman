import time
import sys
from redis_client import redis_client
from .utils import lower_bound

class InvalidTimestampException(Exception):
    pass

class NotFoundException(Exception):
    pass

class KeyValueStorage():
    def save(self, key, value):
        created_at = time.time()
        redis_client.hset(key, created_at, value)

    def get(self, key, timestamp=None):
        if timestamp is None:
            timestamp = sys.maxint
        else:
            try:
                timestamp = float(timestamp)
            except ValueError:
                raise InvalidTimestampException

        created_ats = [float(k) for k in redis_client.hkeys(key)]

        last_created_at = lower_bound(created_ats, timestamp)

        if last_created_at is None:    
            raise NotFoundException
        else:
            return redis_client.hget(key, last_created_at)

