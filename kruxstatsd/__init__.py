# -*- coding: utf-8 -*-
#
# © 2011-2018 Salesforce.com, inc.
#
from __future__ import absolute_import


try:
    from django.conf import settings
except ImportError:
    settings = None

from kruxstatsd.client import StatsClient


__all__ = ['StatsClient', 'kruxstatsd']

# GOTCHA: Setup.py reads this file looking for the __version__ line:
__version__ = '0.3.4'
VERSION = __version__.split('.')

if settings:
    try:
        host = getattr(settings, 'STATSD_HOST', 'localhost')
        port = getattr(settings, 'STATSD_PORT', 8125)
        prefix = getattr(settings, 'STATSD_PREFIX', None)
        env = getattr(settings, 'ENVIRONMENT', None)
        kruxstatsd = StatsClient(prefix, host, port, env)
    except ImportError:
        statsd = None
