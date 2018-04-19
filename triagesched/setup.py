#!/usr/bin/env python

from distutils.core import setup
import os

packages = ['triagesched']

with os.scandir('triagesched') as rit:
    for entry in rit:
        if entry.name[0] not in ('.', '_') and entry.is_dir():
            packages.append(f'{entry.path.replace("/", ".")}')

print(packages)

setup(name='triagesched',
      version='0.1',
      description='Triage schedule',
      author='Daniel',
      author_email='daniel@gtmanfred.com',
      url='https://github.com/gtmanfred/plugins',
      packages=packages,
     )
