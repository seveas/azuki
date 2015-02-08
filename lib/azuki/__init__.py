import logging
import beanstalkc
from functools import wraps
import json
from collections import defaultdict

beanstalks = {'default': {'host': '127.0.0.1', 'port': 11300}}
running_azuki_daemon = False
all_tubes = defaultdict(set)

try:
    from django.core.exceptions import ImproperlyConfigured
    from django.conf import settings
    beanstalks = settings.BEANSTALK_SERVERS
except ImportError:
    django = False
except ImproperlyConfigured:
    django = False

def add_beanstalk(name, host, port=11300):
    beanstalks[name] = {'host': host, 'port': port}

def connect_cached(beanstalk, tube, __cache={}):
    bsc = beanstalks[beanstalk]
    if beanstalk not in __cache:
        __cache[beanstalk] = beanstalkc.Connection(**bsc)
    try:
        __cache[beanstalk].use(tube)
    except Exception:
        # Retry once
        __cache[beanstalk] = beanstalkc.Connection(**bsc)
        __cache[beanstalk].use(tube)
    return __cache[beanstalk]

def beanstalk(tube_or_func='default', beanstalk='default'):
    tube = 'default' if callable(tube_or_func) else tube_or_func
    def decorator(func, tube=tube, beanstalk=beanstalk):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if running_azuki_daemon:
                return func(*args, **kwargs)

            # For normal functions, serialize all arguments
            if not args or not hasattr(args[0], '_meta'):
                data = {
                    'handler':  'function',
                    'module':   func.__module__,
                    'function': func.__name__,
                    'args':     args,
                    'kwargs':   kwargs,
                }
            else:
                self = args[0]; args=args[1:]
                data = {
                    'handler': 'django',
                    'app':     self._meta.app_label,
                    'model':   self._meta.object_name,
                    'method':  hasattr(func, 'func_name') and func.func_name or func.__name__,
                    'pk':      self.pk,
                    'args':    args,
                    'kwargs':  kwargs,
                }

            try:
                data = json.dumps(data)
            except TypeError:
                raise TypeError("Can only queue json-serializable arguments" + repr(data))

            bs = connect_cached(beanstalk, tube)
            return bs.put(data)
        wrapper.stats = lambda: connect_cached(beanstalk, tube).stats_tube(tube)
        all_tubes[beanstalk].add(tube)
        return wrapper

    if callable(tube_or_func):
        return decorator(tube_or_func, tube, beanstalk)
    return decorator
