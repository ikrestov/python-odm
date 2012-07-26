#!/usr/bin/env python

from odm import __version__
from distutils.core import setup

setup(name='python-odm',
      version=__version__,
      description='Object Data Mapping library',
      author='Igor Krestov',
      author_email='igor.krestov@gmail.com',
      url='https://github.com/relic-/python-odm',
      packages=['odm'],
     )
