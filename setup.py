"""
Goal: Configure the package build and distribution

Understanding how to use `enty points` from setup.py
-   http://click.pocoo.org/dev/setuptools/
-   http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
"""

import unittest
from setuptools import setup, find_packages


def olass_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name="olass",

    # https://github.com/pypa/setuptools_scm
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url="https://github.com/ufbmi/olass-client",
    keywords=["entity resolution", "deduplication", "patient linkage"],
    license="MIT",
    author="Andrei Sura",
    author_email="bmi-developers@ad.ufl.edu",
    description='OneFlorida Linkage Submission System (aka ERCA - Entity Resolution Client Application)',  # NOQA
    long_description=open("README.md").read(),

    install_requires=[
        "mysql-connector",
        "requests-oauthlib",
        "SQLAlchemy",
        "setuptools_scm"
    ],
    entry_points={
        "console_scripts": [
            "olass = olass.run:main",
        ],
    },

    tests_require=[
        "mock",
        "pytest-cov"
    ],
    test_suite="setup.olass_test_suite",

    classifiers=[
        'Development Status :: Alpha',
        'Environment :: Console',
        'Intended Audience :: Researchers',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Research :: PHI',
],

)
