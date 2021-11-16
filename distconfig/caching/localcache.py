from cachetools import LFUCache
from .cache import Cache


class LocalLFUCache(Cache):
    def __init__(self, maxsize: int):
        super().__init__(maxsize)
        self.cache: LFUCache = LFUCache(maxsize=maxsize)

    def get(self, key):
        return self.get(key)

    def set(self, key, value):
        self.cache[key] = value
