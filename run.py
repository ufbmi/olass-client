#!/usr/bin/env python
"""
Goal: Implement the application entry point.

@authors:
  Andrei Sura <sura.andrei@gmail.com>
"""

import argparse
from olass.olass_client import OlassClient


if __name__ == "__main__":
    """ Read args """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default='config.py',
                        help="Application config file")
    parser.add_argument('--interactive',
                        default=True,
                        help="When `true` ask for confirmation")

    parser.add_argument('--rows',
                        default=100,
                        help="Number of rows/batch sent to the server")

    args = parser.parse_args()
    app = OlassClient(config_file=args.config,
                      interactive=args.interactive,
                      rows_per_batch=args.rows)
    app.run()
