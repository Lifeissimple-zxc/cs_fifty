import threading
import logging
import time
import random
from typing import Callable
import functools

from . import util


logger = logging.getLogger("wiki")


def cache_check(method: Callable):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # update cache on first call to any of the getters
        if self.last_called is None:
            logger.info("first getter call to %s", method.__name__)
            self.update_cache()
        # update cache if it's too old
        elif (int(time.time()) - self.last_called) > self.cache_ttl_seconds:
            logger.info("cache is outdated, updating")
            self.update_cache()
        return method(self, *args, **kwargs)
    return wrapper

class EntriesCache:
    def __init__(self, entries: list, last_called=0,
                 cache_ttl_seconds=300):
        self.__og_entries = entries
        self.search_entries = set(entries)
        self.last_called = last_called
        self.cache_ttl_seconds = cache_ttl_seconds
        self.lock = threading.Lock()
    
    def update_cache(self):
        with self.lock:
            self.last_called = int(time.time())
            self.__og_entries = util.list_entries()
            self.search_entries = set([entry.lower() for entry in self.__og_entries])

    @cache_check
    def get_entries(self) -> list:
        return self.__og_entries
    
    @cache_check
    def get_random_entry(self) -> str:
        return random.choice(self.__og_entries)
    
    @cache_check
    def search_entry(self, query: str) -> bool:
        return query.lower() in self.search_entries




entries_cache = EntriesCache(entries=util.list_entries())