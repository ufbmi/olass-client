"""
Goal: provide access to the version of the installed package.
"""
import pkg_resources

try:
    __version__ = pkg_resources.require("olass")[0].version
except Exception:
    from setuptools_scm import get_version
    __version__ = get_version()


if __name__ == "__main__":
    print(__version__)
