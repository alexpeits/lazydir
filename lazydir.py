"""
lazydir
~~~~~~~

Simple directory structure validation and creation.

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


def _create_all(config, target):
    for k, v in config.items():
        path = os.path.join(target, k)
        os.mkdir(path)
        if v is None:
            continue
        _create_all(v, path)


def check_and_create(config, target):
    for k, v in config.items():
        path = os.path.join(target, k)
        if not os.path.exists(path):
            os.mkdir(path)
            if v is not None:
                _create_all(v, path)
        elif v is not None:
            check_and_create(v, path)


def _main():
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

    config = get_config(args.config)

    if not os.path.exists(args.target):
        raise ConfigurationError(
            'Target path does not exist: {}'.format(args.target)
        )

    check_and_create(config, args.target)


def main():
    try:
        _main()
    except (ConfigurationError, LazydirError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
