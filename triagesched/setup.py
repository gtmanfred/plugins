#!/usr/bin/env python

from distutils.core import setup
import distutils.dist
from distutils.command.install_data import install_data

import os

packages = ['triagesched']

with os.scandir('triagesched') as rit:
    for entry in rit:
        if entry.name[0] not in ('.', '_') and entry.is_dir() \
                and os.path.isfile(f'{entry.path}/__init__.py'):
            packages.append(f'{entry.path.replace("/", ".")}')


class InstallData(install_data):
    def run(self):
        install_data.run(self)
        for pkgfile in self.outfiles:
            with open(pkgfile, 'r') as tmpfile:
                filedata = tmpfile.read()
            filedata = filedata.replace(
                'localhost:5000',
                'triage.saltstack.com'
            )
            with open(pkgfile, 'w') as tmpfile:
                print(filedata, file=tmpfile)


class TriageDist(distutils.dist.Distribution):
    def __init__(self, attrs=None):
        distutils.dist.Distribution.__init__(self, attrs)
        self.cmdclass.update({'install_data': InstallData})


setup(
    distclass=TriageDist,
    name='triagesched',
    version='0.1.0',
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
