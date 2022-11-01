#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
For information of offt:
    Docs: https://offt.readthedocs.io/en/latest/
    Source Code: https://github.com/ale94mleon/offt
"""

from offt import utils, __version__
import yaml, argparse, inspect, os, sys

def parameterize_cmd():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        help='The configuration yaml file',
        dest='yaml_file',
        type=str)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"offt: {__version__}")