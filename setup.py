from setuptools import setup, find_packages


setup(
    name='kruxstatsd',
    version='0.2.0',
    description='A wrapper around pystatsd that does automatic namespacing',
    packages=find_packages(),
    author='Paul Osman',
    author_email='paul@kruxdigital.com',
    include_package_data=True,
    package_data={'': ['README.rst']},
    install_requires=[
        'statsd==0.3.0',
    ],
    tests_require=[
        'nose==1.1.2',
        'fudge==1.0.3'
    ]
)
