import requests
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from comovotadeputado.cache.constants import CacheConstants

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

def http_fetch_data(cache_key, url): 
    @cache.cache(cache_key, expire=CacheConstants.EXPIRATION_TIME)
    def _fetch_data(url):
        resp = requests.get(url)
        return resp
    resp = _fetch_data(url)
    return resp

    