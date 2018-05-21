# -*- coding: utf-8 -*-
#
# © 2013-2018 Salesforce.com, inc.
#

import re

from setuptools import setup, find_packages

VERSION = "0.3.4"
# URL to the repository on Github.
REPO_URL = 'https://github.com/krux/python-kruxstatsd'
PACKAGE_NAME = 'kruxstatsd'
VERSION_FILE = '{}/__init__.py'.format(PACKAGE_NAME)


# The version info is in kruxstatsd/__init__.py, but that file has code in it
# that we can't execute because it imports packages that aren't installed yet.
# We treat it as a plain text file and extract the value.
# This is a common issue, and this is a common solution:
# PyPA - Python Packaging User Guide - Guides - Single-sourcing the package version
# https://packaging.python.org/guides/single-sourcing-package-version/
def get_version(filename):
    """
    Get __version__ from a Python file without evaluating the file.

    Assumes the version is a SemVer format string
    and that the file has a line of a form more-or-less like:
    __version__ = "MAJOR.MINOR.PATCH"
    https://semver.org/

    :param filename:
    :type filename: str
    :return: str
    """
    version_re = re.compile(
        '''__version__\s*=\s*['"]'''
        '''(?P<major>[\d]+)\.'''
        '''(?P<minor>[\d]+)\.'''
        '''(?P<patch>\d+)'''
        '''(?P<pre>-[0-9A-Za-z-]+)?'''
        '''(?P<meta>\+[[0-9A-Za-z-.]+)?['"]'''
    )
    version = None
    with open(filename, 'r') as f:
        for line in f:
            m = version_re.match(line)
            # There should be 5 groups: MAJOR.MINOR.PATCH-PRERELEASE+META
            # We discard PRERELEASE and META.
            if m and m.group('major') and m.group('minor') and m.group('patch'):
                version = '.'.join([m.group('major'), m.group('minor'), m.group('patch')])
                break
    if not version:
        raise ValueError('Could not extract __version__ from file: %s' % filename)
    return version


__version__ = get_version(VERSION_FILE)

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
