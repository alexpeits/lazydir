# lazydir

Directory structure validation and creation.

## Installation

```
$ git clone https://github.com/alexpeits/lazydir.git
$ cd lazydir
$ mkvirtualenv lazydir
$ pip install .
```

## Usage

The script can be used with a JSON config, and optionally with a YAML
config, if the PyYAML module is installed.

```
usage: lazydir [-h] [-t TARGET] -c CONFIG

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The starting directory (defaults to the current dir).
  -c CONFIG, --config CONFIG
                        The file containing the folder structure.
```

Create a config (json or YAML):

**config.yml**:

```yaml
one:
    two:
    three:
        four:
    five:
```

```
$ mkdir ./target/
$ tree ./target/
target/

0 directories, 0 files
$ lazydir -t ./target/ -c ./config.yml
$ tree ./target/
./target
└── one
    ├── five
    ├── three
    │   └── four
    └── two

5 directories, 0 files
```
