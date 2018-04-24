#!/usr/bin/env python

from distutils.core import setup

setup(
    name='plugin-hub',
    version='0.1.0',
    description='Hub for packing plugins together',
    author='Daniel',
    author_email='daniel@gtmanfred.com',
    url='https://github.com/gtmanfred/plugins',
    packages=['hub', 'hub.mods.tools'],
)

