# -*- coding: utf-8 -*-
#
# © 2011-2018 Salesforce.com, inc.
#

#
# Standard libraries
#
from __future__ import absolute_import
import unittest

#
# Third party libraries
#
from mock import MagicMock, patch
import statsd

#
# Internal libraries
#
from kruxstatsd.client import StatsClient


class StatsClientTest(unittest.TestCase):
    TEST_PREFIX = 'prefix'
    TEST_HOST = 'test.krxd.net'
    TEST_PORT = 12345
    TEST_ENV = 'env'
    TEST_HOSTNAME = 'example'

    def setUp(self):
        self._stats_class = MagicMock()
        self._stats = MagicMock(spec=statsd.StatsClient)
        self._stats_class.return_value = self._stats

        self._socket = MagicMock()
        self._socket.gethostname.return_value = StatsClientTest.TEST_HOSTNAME + '.krxd.net'

        with patch('kruxstatsd.client.statsd.StatsClient', self._stats_class):
            with patch('kruxstatsd.client.socket', self._socket):
                self._client = StatsClient(
                    prefix=StatsClientTest.TEST_PREFIX,
                    host=StatsClientTest.TEST_HOST,
                    port=StatsClientTest.TEST_PORT,
                    env=StatsClientTest.TEST_ENV,
                )

    def test_init(self):
        """
        StatsClient.__init__() correctly sets up all the fields
        """
        self.assertEqual(StatsClientTest.TEST_PREFIX, self._client.prefix)
        self.assertEqual(StatsClientTest.TEST_ENV, self._client.env)

        self._stats_class.assert_called_once_with(
            StatsClientTest.TEST_HOST, StatsClientTest.TEST_PORT
        )
        self.assertEqual(StatsClientTest.TEST_HOSTNAME, self._client.hostname)

    def test_init_no_env(self):
        """
        StatsClient.__init__() correctly raises an exception upon invalid environment
        """
        with self.assertRaises(Exception) as e:
            StatsClient(prefix=StatsClientTest.TEST_PREFIX, env=None)

        self.assertEqual('Env must be set', str(e.exception))

    def test_format_str(self):
        """
        StatsClient._format() correctly returns metric name for string input
        """
        stat = 'foo.bar'
        expected = '.'.join([
            StatsClientTest.TEST_ENV,
            StatsClientTest.TEST_PREFIX,
            stat,
            StatsClientTest.TEST_HOSTNAME,
        ])

        actual = self._client._format(stat)

        self.assertEqual(expected, actual)

    def test_format_list(self):
        """
        StatsClient._format() correctly returns metric name for list input
        """
        stat = ['foo', 15]
        expected = '.'.join(
            [StatsClientTest.TEST_ENV, StatsClientTest.TEST_PREFIX]
            + [str(s) for s in stat]
            + [StatsClientTest.TEST_HOSTNAME]
        )

        actual = self._client._format(stat)

        self.assertEqual(expected, actual)

    def test_format_non_str(self):
        """
        StatsClient._format() correctly returns metric name for non-string input
        """
        stat = 15
        expected = '.'.join([
            StatsClientTest.TEST_ENV,
            StatsClientTest.TEST_PREFIX,
            str(stat),
            StatsClientTest.TEST_HOSTNAME,
        ])

        actual = self._client._format(stat)

        self.assertEqual(expected, actual)

    def test_getattr_args(self):
        """
        StatsClient.__getattr__() correctly re-formats the input value and calls the wrapped client using *args
        """
        stat = 'foo.bar'
        value = 1
        expected = '.'.join([
            StatsClientTest.TEST_ENV,
            StatsClientTest.TEST_PREFIX,
            stat,
            StatsClientTest.TEST_HOSTNAME,
        ])
        # XXX: functools.wraps requires the __name__ to be set
        self._stats.incr.__name__ = 'incr'

        self._client.incr(stat, 1)

        self._stats.incr.assert_called_once_with(expected, value)

    def test_getattr_kwargs(self):
        """
        StatsClient.__getattr__() correctly re-formats the input value and calls the wrapped client using **kwargs
        """
        stat = 'foo.bar'
        value = 1
        expected = '.'.join([
            StatsClientTest.TEST_ENV,
            StatsClientTest.TEST_PREFIX,
            stat,
            StatsClientTest.TEST_HOSTNAME,
        ])
        # XXX: functools.wraps requires the __name__ to be set
        self._stats.incr.__name__ = 'incr'

        self._client.incr(stat=stat, count=1)

        self._stats.incr.assert_called_once_with(stat=expected, count=value)

    def test_getattr_no_args(self):
        """
        StatsClient.__getattr__() correctly re-formats the input value and calls the wrapped client without any arguments
        """
        # XXX: functools.wraps requires the __name__ to be set
        self._stats.pipeline.__name__ = 'pipeline'

        self._client.pipeline()

        self._stats.pipeline.assert_called_once_with()

    def test_getattr_no_call(self):
        """
        StatsClient.__getattr__() correctly returns fields
        """
        self._stats.foo = 1

        self.assertEqual(self._stats.foo, self._client.foo)
