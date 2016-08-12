#!/usr/bin/env python
"""
Goal: Implement the application entry point.

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

import argparse
from olass.olass_client import OlassClient
from olass.version import __version__

DEFAULT_SETTINGS_FILE = 'config/settings.py'


def main():
    """ Read args """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        default=False,
                        action='store_true',
                        help="Show the version number")
    parser.add_argument("-c", "--config",
                        default=DEFAULT_SETTINGS_FILE,
                        help="Application config file")
    parser.add_argument('--interactive',
                        default=True,
                        help="When `true` ask for confirmation")

    parser.add_argument('--rows',
                        default=100,
                        help="Number of rows/batch sent to the server")

    args = parser.parse_args()

    if args.version:
        import sys
        print("olass, version {}".format(__version__))
        sys.exit()

    app = OlassClient(config_file=args.config,
                      interactive=args.interactive,
                      rows_per_batch=args.rows)
    app.run()


if __name__ == "__main__":
    main()
