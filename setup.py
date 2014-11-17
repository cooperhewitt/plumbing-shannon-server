#!/usr/bin/env python

from setuptools import setup

setup(name='plumbing-shannon-server',
      version='0.2',
      description='',
      author='Cooper Hewitt Smithsonian Design Museum',
      url='https://github.com/cooperhewitt/plumbing-palette-server',
      requires=[
      ],
      dependency_links=[
          'https://github.com/cooperhewitt/py-cooperhewitt-flask/tarball/master#egg=cooperhewitt.flask-0.33',
          'https://github.com/cooperhewitt/py-cooperhewitt-roboteyes-shannon/tarball/master#egg=cooperhewitt.roboteyes.shannon-0.2',
      ],
      install_requires=[
          'cooperhewitt.flask',
          'cooperhewitt.roboteyes.shannon',
      ],
      packages=[],
      scripts=[
          'scripts/shannon-server.py',
      ],
      download_url='',
      license='BSD')
