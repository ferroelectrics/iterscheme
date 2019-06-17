#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import re

with open("./iterscheme/__init__.py", "r", encoding="utf8") as init:
    version = re.search(r"__version__ = \"([0-9]+.[0-9]+)\""
						, init.read()).group(1)


setup(name='iterscheme',
      version=version,
      description='Declarative abstraction over nested loops',
      url='https://github.com/ferroelectrics/iterscheme',
      author='Ferroelectrics repository members',
      author_email='rochellesalt@yandex.ru',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)