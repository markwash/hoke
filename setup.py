# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hoke',
    version='0.0.1',
    description='Launchpad blueprint triage for OpenStack Projects',
    long_description=readme,
    author='Mark Washenberger',
    author_email='mark.washenberger@markwash.net',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

