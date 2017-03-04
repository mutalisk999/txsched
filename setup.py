#!encoding=utf8

__author__ = 'mutalisk'

from setuptools import setup
import sys

require_packages = ['setuptools', 'Twisted', 'TwistedSNMP-working', 'pysnmp-se']
if sys.platform == 'nt':
    require_packages.append('pywin32')

setup(name='txsched',
      version='0.1.0',
      description='Twisted Concurrent-Scheduled Framework',
      author='',
      author_email='',
      url='https://github.com/mutalisk999/txsched',
      platforms='any',
      packages=['txsched'],
      install_requires=require_packages,
      zip_safe=False,)
