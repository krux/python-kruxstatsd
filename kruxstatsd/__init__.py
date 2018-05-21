# -*- coding: utf-8 -*-
#
# © 2011-2018 Salesforce.com, inc.
#
from __future__ import absolute_import

from ._version import __version__
from .client import StatsClient

try:
    from django.conf import settings
except ImportError:
    settings = None

VERSION = __version__.split('.')

__all__ = ['StatsClient', 'kruxstatsd']

if settings:
    try:
        host = getattr(settings, 'STATSD_HOST', 'localhost')
        port = getattr(settings, 'STATSD_PORT', 8125)
        prefix = getattr(settings, 'STATSD_PREFIX', None)
        env = getattr(settings, 'ENVIRONMENT', None)
        kruxstatsd = StatsClient(prefix, host, port, env)
    except ImportError:
        statsd = None
