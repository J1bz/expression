#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""j1bz.expression building script."""

from setuptools import setup, find_packages
from setuptools.command.install import install
from pkg_resources import resource_filename
from errno import EEXIST

from os import listdir, makedirs, remove
from os.path import abspath, dirname, join, isfile, isdir
from shutil import copy

from sys import prefix

from re import compile as re_compile, S as re_S

NAME = 'j1bz.expression'  #: library name.

_namepath = NAME.replace('.', '/')

BASEPATH = dirname(abspath(__file__))

# get long description from setup directory abspath
with open(join(BASEPATH, 'README.rst')) as f:
    DESC = f.read()

# Get the version - do not use normal import because it does break coverage
# thanks to the python jira project
# (https://github.com/pycontribs/jira/blob/master/setup.py)
with open(join(BASEPATH, _namepath, 'version.py')) as f:
    stream = f.read()
    regex = r'.*__version__ = \'(.*?)\''
    VERSION = re_compile(regex, re_S).match(stream).group(1)

KEYWORDS = [
    'expression', 'crudity', 'dsl', 'query', 'system', 'access',
    'data', 'crud', 'create', 'delete', 'update', 'read', 'request',
    'grako',
]

DEPENDENCIES = []
with open(join(BASEPATH, 'requirements.txt')) as f:
    DEPENDENCIES = list(line.strip() for line in f.readlines())

DESCRIPTION = 'DSL expressing Crudity requests.'

URL = 'https://github.com/{0}'.format(_namepath)


class CustomInstall(install):
    """
    This custom installation class drops etc conf files in PREFIX/etc.
    """
    def run(self):
        # Here we should run this super class install.run method. But, as
        # it is commented in the run method, a backward compatibility mode
        # twists the behaviour we want. The expected behaviour is
        # do_egg_install.
        install.do_egg_install(self)

        def makedir_p(path):
            try:
                makedirs(path)
            except OSError as exc:
                if exc.errno == EEXIST and isdir(path):
                    pass
                else:
                    raise

        etc = resource_filename(__name__, join('etc', 'j1bz', 'expression',))
        etc_dist = join(prefix, etc)

        print("Copying {} to {}".format(etc, etc_dist))
        makedir_p(etc_dist)
        for f in listdir(etc):
            f_dist = join(etc_dist, f)
            if isfile(f_dist):
                remove(f_dist)

            copy(join(etc, f), etc_dist)

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(exclude=['test.*', '*.test.*']),
    author='j1bz',
    author_email='jbaptiste.braun@gmail.com',
    install_requires=DEPENDENCIES,
    description=DESCRIPTION,
    long_description=DESC,
    include_package_data=True,
    url=URL,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: French',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    test_suite='j1bz',
    entry_points={
        'console_scripts': [
            'expression-cli = j1bz.expression.scripts.expression:main',
        ],
    },
    cmdclass={
        'install': CustomInstall,
    },
    keywords=KEYWORDS
)
