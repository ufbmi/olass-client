"""
Goal: provide access to the version of the installed package.
"""
import pkg_resources
__version__ = pkg_resources.require("olass")[0].version


if __name__ == "__main__":
    print(__version__)
