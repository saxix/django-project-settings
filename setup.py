#!/usr/bin/env python
import os
import codecs
from setuptools import setup, find_packages

dirname = 'project_settings'

app = __import__(dirname)


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r").read()


setup(
    name=app.NAME,
    version=app.get_version(),
    description='Store django settings into Database',
    long_description=read("README"),
    packages=find_packages('.'),
    include_package_data=True,
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ]
)
