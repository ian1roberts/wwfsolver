"""Boggle setup module."""


from codecs import open
from os import path

from setuptools import setup, find_packages

__version__ = 0.1

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wwfsolver',
    version='%s' % __version__,
    author='Ian Roberts',
    author_email='ian.roberts@cantab.net',
    packages=find_packages(exclude=['test*', 'docs']),
    include_package_data=True,
    license='LICENSE.txt',
    description=long_description,
    classifiers=[
        'Development Status :: 3- Alpha',
        'Intended Audience :: Developers',
        'Topic :: Word Games',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['networkx', 'nose'
                      ],
    entry_points={
        'console_scripts': ['wwfs=wwfs.__main__:run_wwfs'],
        },
    test_suite='unittest'
)
