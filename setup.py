#!/usr/bin/env python
import os

from setuptools import find_packages, setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
    SCRIPT_DIR = os.getcwd()

SRC_PREFIX = 'src'


packages = find_packages(SRC_PREFIX)

setup(
      name='cmdline',
      version='0.0.0',
      description='Utilities for consistent command line tools',
      author='Roberto Aguilar',
      author_email='r@rreboto.com',
      package_dir={'': SRC_PREFIX},
      packages=packages,
      long_description=open('README.md').read(),
      url='http://github.com/rca/cmdline',
      license='LICENSE',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Natural Language :: English',
            'Topic :: Utilities'
      ],
      install_requires=[
          'PyYAML>=3',
      ],
)
