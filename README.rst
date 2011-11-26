==========
kruxstatsd
==========

kruxstatsd is a wrapper library around `pystatsd`_. It will format stats based
on a provided prefix (just like `pystatsd`), environment, and the host the
client is running on. For example, incrementing the following stat on a host
called ``ops-dev004.krxd.net``: ::

  import kruxstatsd

  k = kruxstatsd.StatsClient('js', env='stage')
  k.incr('foo')

will create a stat named 'stage.js.foo.ops-dev004'.

Usage
-----

To use ``kruxstatsd``, simply import it instead of ``pystatsd``. The interface
is exactly the same. Context managers will also continue to work: ::

  with k.timer('expensive_op'):
      func()

.. _pystatsd: https://github.com/jsocol/pystatsd
