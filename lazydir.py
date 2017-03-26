"""
lazydir
~~~~~~~

Simple directory structure validation and creation.

TODO:
    - implementation
    - tests
    - cli interface
    - conf types
    - usage docs

"""

from __future__ import print_function

import os
import sys
import argparse


FT_MAP = {}


class ConfigurationError(Exception):
    pass


class LazydirError(Exception):
    pass


def ext(suffix):
    def decorator(func):
        FT_MAP[suffix] = func
        return func
    return decorator


@ext('json')
def load_json(config_path):
    import json
    with open(config_path) as f:
        return json.load(f)


@ext('yml')
def load_yaml(config_path):
    try:
        import yaml
    except ImportError:
        raise ConfigurationError('PyYAML module is not available')
    with open(config_path) as f:
        return yaml.load(f)


def get_config(config_path):
    if not os.path.exists(config_path):
        raise ConfigurationError('Path does not exist: {}'.format(config_path))
    config_file = os.path.basename(config_path)
    _, config_ext = os.path.splitext(config_file)
    config_ext = config_ext.strip('.')
    return FT_MAP[config_ext](config_path)


def check_and_create(config):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--target',
        dest='target', action='store', type=str, default=os.curdir,
        help='The starting directory (defaults to the current dir).'
    )
    parser.add_argument(
        '-c', '--config',
        dest='config', action='store', type=str, required=True,
        help='The file containing the folder structure.'
    )
    args = parser.parse_args()

    try:
        config = get_config(args.config)
    except ConfigurationError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        check_and_create(config)
    except LazydirError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
