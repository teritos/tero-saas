"""Setup file."""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()


REQUIREMENTS = [
    'numpy',
    'scikit-image',
    'boto3',
    'scipy',
    'imagehash',
]

TEST_REQUIREMENTS = [
    'ipython',
]

setup(
    name='libtero',
    version='0.1.0',
    description="Tero libs",
    long_description=README + '\n\n' + HISTORY,
    author=" ",
    author_email=' ',
    url='https://github.com/edvm/tero',
    packages=[
        'libtero',
    ],
    package_dir={'libtero':
                 'libtero'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='tero',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
