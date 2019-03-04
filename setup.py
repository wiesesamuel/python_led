#!/usr/bin/env python3

import sys
from setuptools import setup


requires = [
    'bottle',
    'bjoern',
    'RPi.GPIO'
]
if sys.version_info < (3, 7):
    sys.exit("Python 3.7 or newer is required to run this program.")

setup(
    name='lightstorm',
    python_requires=">3.7",
    description='Web LED Controller',
    long_description='Web Interface for controlling GPIO (and more) connected LEDs on a Raspberry PI.',
    version='3.0',
    entry_points={
        'console_scripts': ['lightstorm=lightstorm:main'],
    },
    packages=['lightstorm'],
    url='',
    download_url='',
    author='samuelwiese',
    author_email='',
    install_requires=requires,
)
