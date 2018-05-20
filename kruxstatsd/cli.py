# -*- coding: utf-8 -*-
#
# © 2011-2018 Salesforce.com, inc.
#

#
# Standard libraries
#

import time

#
# Third party libraries
#

from argparse import ArgumentParser

#
# Internal libraries
#

import kruxstatsd


class Application(object):
    """
    A CLI application designed for development testing of kruxstatsd.
    The goal of this class is to provide a quick and dirty client of kruxstatsd to be used during development.

    This does not replace a proper unit test.
    Also, unlike other CLI applications for krux libraries, this class is not designed to be inherited by other
    CLI as a quick bootstrap of kruxstatsd. Use krux.cli.Application for that.
    """

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
        self.stats.incr('test', 2)
        self.stats.incr(stat='kwargs_test', count=3)
        self.stats.gauge('test', 4)
        self.stats.gauge(1, 5)
        self.stats.gauge(['list', 'test'], 6)
        self.stats.gauge(stat=['list', 'kwargs', 1], value=7)
        with self.stats.timer('test'):
            time.sleep(1)


def main():
    Application().run()


# Run the application stand alone
if __name__ == '__main__':
    main()
