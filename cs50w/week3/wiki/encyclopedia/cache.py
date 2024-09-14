import threading
import logging
import time

from . import util


logger = logging.getLogger("wiki")


class EntriesCache:
    def __init__(self, entries: list, last_called=0,
                 cache_ttl_seconds=300):
        self.entries = entries
        self.last_called = last_called
        self.cache_ttl_seconds = cache_ttl_seconds
        self.lock = threading.Lock()
    
    def update_cache(self):
        with self.lock:
            self.last_called = int(time.time())
            self.entries = util.list_entries()

    def get_entries(self) -> list:
        if self.last_called is None:
            logger.info("first call to cache.get_entries()")
            self.update_cache()
        # getting here means it's not our first call to get_entries()
        # so we check if we can use cache
        if (int(time.time()) - self.last_called) > self.cache_ttl_seconds:
            logger.info("cache is outdated, updating")
            self.update_cache()
        return self.entries


entries_cache = EntriesCache(entries=util.list_entries())