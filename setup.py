#!/usr/bin/env python
import os
import sys

from codecs import open

import setuptools


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

package_name = 'py_bingads'

packages = [package_name] + [
    '%s.%s' % (package_name, item)
    for item in
    setuptools.find_packages('py_bingads')
]

setuptools.setup(
    name=package_name,
    version='0.1.0',
    description='A Python wrapper for Bing Ads API',
    long_description=readme + '\n\n' + history,
    author='Julie MacDonell, Raul Taranu',
    author_email='julie.macdonell@stylight.com, raul.taranu@stylight.com',
    url='http://github.com/stylight/py-bingads',
    license='MIT License',
    packages=packages,
    package_data={'': ['*.rst']},
    include_package_data=True,
    install_requires=[
        'bingads==11.5.5.1',
        'six',
    ],
    keywords='python bingads bing ads api'
)
