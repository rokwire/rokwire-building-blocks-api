#  Copyright 2020 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import bson.json_util
import diskcache
import json
import os

# Populate cache defaults here instead of config.py because they are
# used in function decorators before the config.py is loaded into the
# Flask app environment
CACHE_DIRECTORY       = os.getenv('CACHE_DIRECTORY', '/var/cache/app')
CACHE_SETTINGS        = json.loads(os.getenv('CACHE_SETTINGS', '{}'))
CACHE_GET_DEFAULT     = os.getenv("CACHE_GET_DEFAULT", '{"expire": 600}')
CACHE_GET_EVENTS      = json.loads(os.getenv("CACHE_GET_EVENTS", CACHE_GET_DEFAULT))
CACHE_GET_EVENT       = json.loads(os.getenv("CACHE_GET_EVENT", CACHE_GET_DEFAULT))
CACHE_GET_EVENTIMAGES = json.loads(os.getenv("CACHE_GET_EVENTIMAGES", CACHE_GET_DEFAULT))
CACHE_GET_CATEGORIES  = json.loads(os.getenv("CACHE_GET_CATEGORIES", CACHE_GET_DEFAULT))

CACHE_SETTINGS.setdefault('size_limit', 3.5 * 1025 * 1024 * 1024) # 3.5GB cache
cache = diskcache.Cache(
    directory=CACHE_DIRECTORY,
    **CACHE_SETTINGS
)


def memoize(*args, **kwargs):
    """
    Basic memoize function that uses our cache and wraps memoize_stampede.
    It takes all the same arguments as memoize_stampede, except do not
    specify the cache argument.
    """
    def decorator(func):
        return diskcache.memoize_stampede(cache, *args, **kwargs)(func)

    return decorator


def memoize_query(*args, **kwargs):
    """
    Memoize a function that takes a MongoDB query as its first
    argument. This decorator takes all the same arguments as
    memoize_stampede, except do not specify the cache argument.
    """
    def decorator(func):
        wrapper = diskcache.memoize_stampede(cache, *args, **kwargs)(func)

        old_cache_key = wrapper.__cache_key__
        def __cache_key__(query, *args, **kwargs):
            """
            Get a cache key where the first argument to the function is a
            MongoDB query. It does this by using the BSON dumps util.
            """
            query_json = bson.json_util.dumps(query, sort_keys=True)
            return old_cache_key(query_json, *args, **kwargs)
        wrapper.__cache_key__ = __cache_key__

        return wrapper

    return decorator
