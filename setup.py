# -*- coding: utf-8 -*-
#
# © 2013-2018 Salesforce.com, inc.
#

from setuptools import setup, find_packages

VERSION = "0.3.4"
# URL to the repository on Github.
REPO_URL = 'https://github.com/krux/python-kruxstatsd'
PACKAGE_NAME = 'kruxstatsd'
VERSION_FILE = '{}/version.py'.format(PACKAGE_NAME)

# Retrieve __version__ from file without evaluating any other part of the module.
__version__ = None  # squelch code inspection
execfile(VERSION_FILE)
print(__version__)

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', __version__))


setup(
    name=PACKAGE_NAME,
    version=__version__,
    author='Paul Osman',
    maintainer='Paul Lathrop',
    maintainer_email='paul@krux.com',
    description='Wrapper around pystatsd with automatic namespacing',
    url=REPO_URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'statsd',
    ],
    tests_require=[
        'coverage',
        'mock',
        'nose',
        'fudge',
    ],
    entry_points={
        'console_scripts': [
            'kruxstatsd-test = kruxstatsd.cli:main',
        ],
    }
)
