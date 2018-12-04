import inspect
import os
import sys

CONFIG_ROOT = 'CMDLINE_CONFIG_ROOT'


def find_config_root(path=sys.argv[0]):
    """
    Finds config root relative to the given file path
    """
    dirname = os.path.dirname(path)
    lastdirname = None

    while dirname != lastdirname:
        config_root = os.path.join(dirname, 'config')
        if os.path.exists(config_root):
            return config_root

        lastdirname, dirname = dirname, os.path.dirname(dirname)


def get_config_paths(filename=None, reversed=False):
    config_paths = []

    script_name = os.path.basename(sys.argv[0])

    package = inspect.stack()[-2].frame.f_globals['__package__']
    data_path = os.path.join('cmdline', package)

    config_root = os.environ.get(CONFIG_ROOT)
    if config_root:
        if not os.path.exists(config_root):
            raise OSError('{}={} does not exist'.format(CONFIG_ROOT, config_root))

        config_locations = (
            config_root,
        )
    else:
        config_locations = ()

    # handle debian/ubuntu strangeness where `pip install` will install
    # to /usr/local, yet sys.prefix is /usr
    prefix = sys.prefix
    if not os.path.exists(os.path.join(prefix, data_path)):
        _prefix = os.path.join(prefix, 'local')
        if os.path.exists(os.path.join(_prefix, data_path)):
            prefix = _prefix

    for dirpath in (
            os.path.join(prefix, data_path),
            os.path.join(prefix, 'etc', script_name),
            os.path.expanduser('~/.{}'.format(script_name)),
            ) + config_locations:
        full_path = dirpath

        if filename:
            full_path = os.path.join(full_path, filename)

        config_paths.append(full_path)

    if config_root and reversed:
        return config_paths[-1::-1]

    return config_paths
