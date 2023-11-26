#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
For information of TOFF:
    Docs: https://TOFF.readthedocs.io/en/latest/
    Source Code: https://github.com/ale94mleon/TOFF
"""

import argparse
import warnings

import yaml

from toff import Parameterize, __version__


def __parameterize_cmd():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        help='The configuration yaml file',
        dest='yaml_file',
        type=str)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"toff: {__version__}")
    args = parser.parse_args()

    print(f"You are using toff:{__version__}")
    with open(args.yaml_file, 'r') as c:
        Config = yaml.safe_load(c)
    InitKwargs = ['force_field_code', 'ext_types', 'hmr_factor', 'overwrite', 'safe_naming_prefix', 'out_dir']
    CallKwargs = ['input_mol', 'mol_resi_name']

    UserExtraNonValidKwargs = set(Config.keys()) - set(InitKwargs + CallKwargs)
    if 'input_mol' not in Config:
        raise RuntimeError("Not input_mol parameter provided in the configuration yaml file.")
    elif UserExtraNonValidKwargs:
        warnings.warn(f"Parameters: [{' '.join(UserExtraNonValidKwargs)}] is/are not valid and therefore discarded.")

    UserInitKwargs = {kwarg: Config[kwarg] for kwarg in Config if kwarg in InitKwargs}
    UserCallKwargs = {kwarg: Config[kwarg] for kwarg in Config if kwarg in CallKwargs}
    parameterizer = Parameterize(**UserInitKwargs)
    print(parameterizer)
    parameterizer(**UserCallKwargs)
