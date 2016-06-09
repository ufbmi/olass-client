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
    args = parser.parse_args()
    app = OlassClient(config_file=args.config)
    app.run()
