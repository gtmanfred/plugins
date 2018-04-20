#!/usr/bin/env python

from distutils.core import setup
import os

packages = ['triagesched']

with os.scandir('triagesched') as rit:
    for entry in rit:
        if entry.name[0] not in ('.', '_') and entry.is_dir() and os.path.isfile(f'{entry.path}/__init__.py'):
            packages.append(f'{entry.path.replace("/", ".")}')

print(packages)

setup(
    name='triagesched',
    version='0.1',
    description='Triage schedule',
    author='Daniel',
    author_email='daniel@gtmanfred.com',
    url='https://github.com/gtmanfred/plugins',
    packages=packages,
    include_package_data=True,
    data_files=[
        ('share/nginx/html/', ['triagesched/html/index.html']),
        ('share/nginx/html/edit/', ['triagesched/html/edit/index.html']),
    ],
)
