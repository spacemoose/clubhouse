#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.0'


setup(
    name='clubhouse',
    version=VERSION,
    description='A python client library for the clubhouse.io api',
    long_description=open('README.rst').read(),
    author='Mahmoud Abdelkader',
    url='https://github.com/mahmoudimus/clubhouse',
    packages=find_packages(exclude=['tests', '*.test', '*.test.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'attrs>=17.4.0,<17.5',
        'requests>=2.0,<3.0',
        'marshmallow'#>=3.0,<4' I took out versioning to allow release candidate install
    ],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
