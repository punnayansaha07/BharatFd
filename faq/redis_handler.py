import redis
from django.core.cache import cache
from django.db import transaction

class RedisHandler:
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)

    def get_cache(self, key):
        """ Get data from Redis cache """
        return self.client.get(key)

    def set_cache(self, key, value, timeout=3600):
        """ Set data to Redis cache with timeout """
        self.client.setex(key, timeout, value)

    @transaction.atomic
    def set_cache_with_transaction(self, key, value, timeout=3600):
        """ Set data with atomic transaction """
        self.set_cache(key, value, timeout)
