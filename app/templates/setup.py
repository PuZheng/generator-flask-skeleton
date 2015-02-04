# -*- coding: UTF-8 -*-

from distutils.core import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys
import re

NAME = u"<%= projectName %>"
PACKAGE = u"<%= packageName %>"
DESCRIPTION = ""
AUTHOR = ""
AUTHOR_EMAIL = ""
URL = ""
DOC = __import__(PACKAGE).__doc__
VERSION = '0.1'
LICENSE = 'MIT'


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)

install_requires = []
dependency_links = []

for l in open('requirements.txt').xreadlines():
    m = re.match("-e (git|svn|hg|bzr)\+(?P<link>.*)#(?P<egg>.+)", l.strip())
    if m:
        install_requires.append(m.groupdict()['egg'])
        dependency_links.append(m.groupdict()['link'])
    else:
        install_requires.append(l.strip())


setup(
    name=NAME,
    version=VERSION,
    long_description=DOC,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
