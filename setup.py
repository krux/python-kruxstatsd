# -*- coding: utf-8 -*-
#
# © 2013, 2014 Krux Digital, Inc.
#

from setuptools import setup, find_packages

import os


# We use the version to construct the DOWNLOAD_URL.
VERSION = '0.3.0'

# URL to the repository on Github.
REPO_URL = 'https://github.com/krux/python-kruxstatsd'

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))


setup(
    name='kruxstatsd',
    version=VERSION,
    author='Paul Osman',
    maintainer='Paul Lathrop',
    maintainer_email='paul@krux.com',
    description='Wrapper around pystatsd with automatic namespacing',
    url=REPO_URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'statsd==3.2.1',
        'argparse==1.4.0',
    ],
    tests_require=[
        'coverage==4.2',
        'mock==1.1.2',
        'nose==1.3.7',
        'fudge==1.1.0',
    ],
    entry_points={
        'console_scripts': [
            'kruxstatsd-test = kruxstatsd.cli:main',
        ],
    }
)
