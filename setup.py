"""
OLASS Client
------------

OneFlorda Linkage Submission System (OLASS) client software
<https://github.com/ufbmi/olass-client> is designed to compute hashes of the
specific patient data elements and submit them to the OLASS server
<https://github.com/ufbmi/olass-server> to achieve de-duplication.

The client authorizes using the OAuth2 protocol on the server, submits the
hashes, and receives back an uniqueidentifier (UUID) for each patient.
The UUID is used later for submission of medical records such as
demographics, procedures, diagnoses, vitals, lab results.

"""
import unittest
from pip.req import parse_requirements
from setuptools import setup, find_packages


def olass_test_suite():
    """
    Prepare a test-suite callable with:
        python setup.py test
    """
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


def load_requirements():
    """ Helps to avoid storing requirements in more than one file"""
    reqs = parse_requirements('requirements-to-freeze.txt', session=False)
    reqs_list = [str(ir.req) for ir in reqs]
    return reqs_list


# Configure the package build and distribution
#   @see https://github.com/pypa/setuptools_scm
#   @see http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool  # NOQA
#
# To record the files created use:
#   python setup.py install --record files.txt

setup(
    name="olass",

    use_scm_version=True,
    url="https://github.com/ufbmi/olass-client",
    license="MIT",
    author="Andrei Sura",
    author_email="bmi-developers@ad.ufl.edu",
    description="OneFlorida Linkage Submission System",
    long_description=__doc__,
    keywords=["entity resolution", "deduplication", "record linkage"],

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms="any",  # darwin, linux2
    setup_requires=["setuptools_scm"],
    install_requires=load_requirements(),
    # tests_require=["mock", "pytest-cov"],  # requirements included above
    test_suite="setup.olass_test_suite",

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],

    entry_points={
        "console_scripts": [
            "olass = olass.run:main",
        ],
    },
)
