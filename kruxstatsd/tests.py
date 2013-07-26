import kruxstatsd
import socket
import fudge
from fudge.inspector import arg

import statsd

hostname = socket.gethostname().split('.')[0]
env      = 'prod'
prefix   = 'js'


def mock_statsd_method(kls, stat, count=1, rate=1):
    assert stat.startswith('%s.%s' % (env, prefix))
    assert stat.endswith(hostname)


def test_stats_format_incr():
    fudge.patch_object(statsd.StatsClient, 'incr', mock_statsd_method)
    k = kruxstatsd.StatsClient('js', env='prod')
    k.incr('foo')


def test_stats_format_timing():
    fudge.patch_object(statsd.StatsClient, 'timing', mock_statsd_method)
    k = kruxstatsd.StatsClient('js', env='prod')
    k.timing('foo.bar.baz')


@fudge.patch('kruxstatsd.tests.mock_statsd_method')
def test_context_manager(fake):
    fudge.patch_object(statsd.StatsClient, 'timing', mock_statsd_method)
    k = kruxstatsd.StatsClient('js', env='prod')
    fake.expects_call().with_args(
        'prod.js.mytimer.%s' % (hostname,), arg.any(), 1)
    with k.timer('mytimer'):
        assert True


def test_incorrect_args():
    k = kruxstatsd.StatsClient('js', env='prod')
    try:
        k.incr()
    except TypeError:
        assert True
    except:
        assert False  # only exception thrown should be a TypeError
