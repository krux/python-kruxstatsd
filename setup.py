from setuptools import setup, find_packages

import kruxstatsd


setup(
    name='kruxstatsd',
    version=kruxstatsd.__version__,
    description='A wrapper around pystatsd that does automatic namespacing',
    packages=find_packages(),
    author='Paul Osman',
    author_email='paul@kruxdigital.com',
    include_package_data=True,
    package_data={'': ['README.rst']},
)
