# -*- coding: utf-8 -*-
#
# © 2013 Krux Digital, Inc.
#

from pip.req    import parse_requirements
from setuptools import setup, find_packages

import os


# We use the version to construct the DOWNLOAD_URL.
VERSION      = '0.2.2'

# URL to the repository on Github.
REPO_URL     = 'https://github.com/krux/python-kruxstatsd'

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))

# We want to install all the dependencies of the library as well, but we
# don't want to duplicate the dependencies both here and in
# requirements.pip. Instead we parse requirements.pip to pull in our
# dependencies.
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS = os.path.join(BASE_DIR, 'requirements.pip')

# A requirement file can contain comments (#) and can include some other
# files (--requirement or -r), so we need to use pip's parser to get the
# final list of dependencies.
DEPENDENCIES = [unicode(package.req)
                for package in parse_requirements(REQUIREMENTS)]


setup(
    name                 = 'kruxstatsd',
    version              = VERSION,
    author               = 'Paul Osman',
    maintainer           = 'Paul Lathrop',
    maintainer_email     = 'paul@krux.com',
    description          = 'Wrapper around pystatsd with automatic namespacing',
    url                  = REPO_URL,
    download_url         = DOWNLOAD_URL,
    license              = 'MIT',
    packages             = find_packages(),
    install_requires     = DEPENDENCIES,
    tests_require        = [
        'nose==1.1.2',
        'fudge==1.0.3'
    ]
)
