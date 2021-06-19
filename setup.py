# -*- coding: utf-8 -*-
""" JioFiber setup.py script """

# JioFiber
from jiofiber import __version__

# system
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name='jioFiber-Api',
    version='0.1.0',
    description='Unoffical JioFiber Router API to access it via python',
    author='Shreyas Kapale',
    author_email='kapale.shreyas@gmail.com',
    packages=['jiofiber','jiofiber.test'],
    url='http://github.com/shreyaskapale/jiofiber-api',
    long_description=open('README.txt').read(),
    license='MIT',
    python_requires='>=3.6.0',
    install_requires=['requests','beautifulsoup4'],
    test_suite='jiofiber.test',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
      ],
)
