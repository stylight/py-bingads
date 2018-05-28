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
    version='0.1.2',
    description='Wraps BingAds Python SDK to make it more Pythonic',
    long_description=readme + '\n\n' + history,
    author='Julie MacDonell',
    author_email='julie.macdonell@stylight.com',
    url='https://github.com/stylight/python-bingads',
    download_url='https://github.com/stylight/python-bingads/archive/0.2.tar.gz',
    license='MIT License',
    packages=packages,
    package_data={'': ['*.rst']},
    include_package_data=True,
    install_requires=[
        'bingads==11.5.8',
        'six',
    ],
    keywords='python bingads bing ads api'
)
