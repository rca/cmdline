# cmdline

NOTE: this is proof-of-concept code and is no longer maintained.

The cmdline package provides a standard way to specify and override command settings and logging configuration.  Using cmdline setttings is as simple as creating a `settings.yml`:
```
REMOTE_ADDR:
  default: 'https://example.com/'
  help: the remote address
```
and compiling the settings in your main program:
```
from cmdline import SettingsParser, settings


def main():
    SettingsParser.compile_settings()

    remote = settings.REMOTE_ADDR

    print('remote addr:', remote)


if __name__ == '__main__':
    sys.exit(main())
```
Your program can then be called in any of the following ways:
```
$ remote
remote addr: https://example.com/
$ export REMOTE_ADDR=https://env.example.com/
$ remote
remote addr: https://env.example.com/
$ remote --remote-addr=https://arg-takes-precedence.example.com/
remote addr: https://arg-takes-precedence.example.com/
```

## Installation
```
pip install cmdline
```

## Settings
Settings are configured in an overlaid fashion starting with a root configuration packaged with the application.  Standard [argparse](https://docs.python.org/3/library/argparse.html) options are used to configure settings.

### Override defaults
The packaged settings can be overridden by additional settings files on the filesystem, environment variables, and finally command line arguments.  For a command named `remote` order in which they are applied are:

- packaged settings
- <sys.prefix>/etc/remote/settings.yml
- ~/.remote/settings.yml
- environment variables
- command line arguments

Environment variables map exactly to the name of the setting, i.e. the environment variable `REMOTE_ADDR` configures the `REMOTE_ADDR` setting.

Command line arguments are lowercase-dashed versions of the setting, for instance, the command line argument `--remote-addr` configures the `REMOTE_ADDR` setting.

### Subcommands
The settings parser supports [argparse subcommands](https://docs.python.org/3/library/argparse.html#sub-commands).  A setting can be configured to be for a subcommand by adding a `_subcommand` key to the setting's options.  For example:
```
COPY_FORCE
  default: no
  _subcommand: copy
```
The `_SUBCOMMAND` setting contains the name of the subcommand the command was run with.

### Documentation
Command descriptions and help text can be added in a `_COMMANDS` section.  The `_main` will set the description for the main program.  Any other keys will correspond to a subcommand by the same name.  For example, below sets the description for the main program and the description and help text for the `copy` subcommand:
```
_COMMANDS:
  _main:
    description: >
      this is main description and can be a very long string
      that covers multiple lines
  copy:
    description: >
      this is copy subcommand description and can be a very long string
      that covers multiple lines
    help: copy files
```
### Type conversion
Settings can be converted to a particular type using argparse's `type` setting.  For example setting `type: int` will convert the setting into an integer.  This is done by using Python's built-in `int()` function.

When `type` is a dotted string, the given function will be imported and used.  For example, setting `type: convesion.convert_bool` will call the `convert_bool()` function in the [conversion](https://pypi.python.org/pypi/conversion) package.

## Logging
Similarly, logging is configured through Python's `logging.config.dictConfig()` function.  More info on dictconfig is at [docs.python.org](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig); an example is below.  This configuration sets a `console` handler that sends logs to stdout and a `null` handler that throws away logs.  The default logging configuration is to log WARN level and higher messages to the console, which is setup by the `root` logger, and two additional loggers are configured for the `mypkg.foo` and `mypkg.bar` loggers, where the loglevel for `mypkg.foo` is set to DEBUG and `mypkg.bar` is thrown out altogether.

```
version: 1
disable_existing_loggers: False

formatters:
  simple:
    format: "%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s"


handlers:
  console:
    class: logging.StreamHandler
    level: WARN
    formatter: simple
    stream: ext://sys.stdout

  "null":
    class: logging.NullHandler


loggers:
  mypkg.foo:
    level: DEBUG
    handlers: [console]
    propagate: no

  mypkg.bar:
    handlers: ["null"]
    propagate: no


root:
  level: WARN
  handlers: [console]
```
Once the configuration is written, logging is configured by calling the `setup_logging()` function:
```
import logging
from cmdline import setup_logging


def main():
    setup_logging()

    logging.getLogger(__name__).warning('ello')


if __name__ == '__main__':
    sys.exit(main())
```
### Log level environment
The only logging configuration that can be updated outside the configuration file is the default log level, which can be changed with the environment variable `LOG_LEVEL`; for example, `LOG_LEVEL=debug remote`.

## File location
Create a directory named `config`.  In that directory, create the files `logconfig.yml` and `settings.yml`.  A bare-bones `setup.py` that installs these files correctly is below:
```
#!/usr/bin/env python 
import os

from setuptools import setup


def get_data_files(base):
    for dirpath, dirnames, filenames in os.walk(base):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


data_files = [
    ('config', list(get_data_files('config'))),
]

setup(name='remote',
      version='0.0.1',
      packages=['remote'],
      data_files=data_files,
      entry_points = {
          'console_scripts': [
              'remote = remote.command:main',
          ],
      },
)
```
The file structure for the `setup.py` above looks like:
```
root_dir/
+- remote/
|  +- __init__.py
|  +- command.py
+- config/
|  +- logconfig.yml
|  +- settings.yml
+- setup.py
```
## Config root environment variable
Setting the environment variable `CMDLINE_CONFIG_ROOT` will make the given path the primary config location for settings and logging.
