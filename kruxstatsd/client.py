import socket
from functools import wraps

import statsd


class StatsClient(object):

    def __init__(self, prefix, host='localhost', port=8125, env=None):
        """Create a wrapper around ``pystatsd`` that abstracts away naming.

        Clients don't need to know anything about our stats naming conventions,
        instead they just use this library instead of ``pystatsd``.
        """

        self.prefix = prefix
        self.env = env

        if env is None:
            raise Exception('Env must be set')

        # we intentionally don't send the prefix to ``statsd.StatsClient``
        # because all formatting happens in this library before sending
        # it to pystatsd.
        self.client = statsd.StatsClient(host, port)
        self.hostname = socket.gethostname().split('.')[0]

    def _format(self, stat):
        """Format a stats string with the environment, prefix and hostname."""
        return '%s.%s.%s.%s' % (
            self.env, self.prefix, stat, self.hostname)

    def __getattr__(self, attr):
        """Proxies calls to ``statsd.StatsClient`` methods.

        Intercept and properly format the ``stat`` param.
        """
        attr = getattr(self.client, attr)
        if callable(attr):
            @wraps(attr)
            def wrapper(*args, **kwargs):
                if not args:
                    return attr(*args, **kwargs)
                return attr(self._format(args[0]), *args[1:], **kwargs)
            return wrapper
        return attr
