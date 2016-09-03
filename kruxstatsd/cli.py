# -*- coding: utf-8 -*-
#
# © 2011-2016 Krux Digital, Inc.
#

#
# Standard libraries
#

import sys
import random
import time

#
# Third party libraries
#

import statsd
from argparse import ArgumentParser

#
# Internal libraries
#

import kruxstatsd


class Application(object):
    NAME = 'kruxstatsd-test'
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 8125
    DEFAULT_ENVIRONMENT = 'dev'

    def __init__(self, name=NAME, *arg, **kwargs):
        self.name = name

        self.parser = self.get_parser(description=self.name)
        self.add_cli_arguments(self.parser)
        self.args = self.parser.parse_args()

        self.stats = kruxstatsd.StatsClient(
            prefix=self.name,
            host=self.args.host,
            port=self.args.port,
            env=self.args.environment,
        )

    def get_parser(self, description):
        return ArgumentParser(description=description)

    def add_cli_arguments(self, parser):
        parser.add_argument(
            '-H', '--host',
            default=self.DEFAULT_HOST,
            help='Statsd host to send statistics to. (default: %(default)s)',
        )
        parser.add_argument(
            '-p', '--port',
            default=self.DEFAULT_PORT,
            help='Statsd port to send statistics to. (default: %(default)s)',
        )
        parser.add_argument(
            '-e', '--environment',
            default=self.DEFAULT_ENVIRONMENT,
            help='Statsd environment. (default: %(default)s)',
        )

        return parser

    def run(self):
        self.stats.incr('test', random.randint(1, 10))
        self.stats.incr(stat='kwargs_test', count=random.randint(1, 10))
        self.stats.gauge('test', random.randint(1, 10))
        self.stats.gauge(1, random.randint(1, 10))
        self.stats.gauge(['list', 'test'], random.randint(1, 10))
        self.stats.gauge(stat=['list', 'kwargs', 1], value=random.randint(1, 10))
        with self.stats.timer('test'):
            time.sleep(random.randint(1, 5))


def main():
    Application().run()


# Run the application stand alone
if __name__ == '__main__':
    main()
