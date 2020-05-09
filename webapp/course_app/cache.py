import cachetools
from threading import Lock

cache = cachetools.TTLCache(100, 60 * 60)
cache_lock = Lock()
