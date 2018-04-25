#!/usr/bin/env python

from distutils.core import setup

import os

packages = ['hub']

with os.scandir('hub/mods') as rit:
    for entry in rit:
        if entry.name[0] not in ('.', '_') and entry.is_dir():
            packages.append(f'{entry.path.replace("/", ".")}')

setup(
    name='plugin-hub',
    version='0.1.0',
    description='Hub for packing plugins together',
    author='Daniel',
    author_email='daniel@gtmanfred.com',
    url='https://github.com/gtmanfred/plugins',
    packages=packages,
)
