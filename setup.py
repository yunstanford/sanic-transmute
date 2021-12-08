#!/usr/bin/env python
import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'transmute-core>=1.9',
    'sanic',
]

tests_require = []

setup(name='sanic-transmute',
      version='0.1.4',
      description='',
      long_description=open(README_PATH).read(),
      author='Yun Xu',
      author_email='yunxu1992@gmail.com',
      url='https://github.com/yunstanford/sanic-transmute/',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ]
)
