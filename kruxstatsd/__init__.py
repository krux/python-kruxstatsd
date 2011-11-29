try:
    from django.conf import settings
except ImportError:
    settings = None

from client import StatsClient


__all__ = ['StatsClient', 'kruxstatsd']

VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))

if settings:
    try:
        host = getattr(settings, 'STATSD_HOST', 'localhost')
        port = getattr(settings, 'STATSD_PORT', 8125)
        prefix = getattr(settings, 'STATSD_PREFIX', None)
        env = getattr(settings, 'ENVIRONMENT', None)
        kruxstatsd = StatsClient(prefix, host, port, env)
    except ImportError:
        statsd = None
