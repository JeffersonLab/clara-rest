#!/usr/bin/env python
# coding=utf-8

import os
import claraweb
from setuptools import find_packages, setup
from distutils.core import Command


class RESTCleaner(Command):
    user_options = []

    def initialize_options(self):
        """Nothing here"""
        pass

    def finalize_options(self):
        """Nothing here"""
        pass

    def run(self):
        os.system('rm -vrf ./.cache ./.eggs ./build ./dist')
        os.system('rm -vrf ./*.tgz *.egg-info')
        os.system('find . -name "*.pyc" -exec rm -vrf {} \;')
        os.system('find . -name "__pycache__" -exec rm -rf {} \;')

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    README = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as license_file:
    LICENSE = license_file.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='clara-rest',
    version=claraweb.__version__,
    packages=find_packages(),
    include_package_data=True,
    license=LICENSE,
    description='Clara Framework: REST Server for registration and monitoring',
    long_description=README,
    url='https://claraweb.jlab.org/',
    author='Ricardo Oyarzun',
    author_email='oyarzun@jlab.org',
    cmdclass={'clean': RESTCleaner,},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
