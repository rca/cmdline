import os
import sys

CONFIG_ROOT = 'CMDLINE_CONFIG_ROOT'

config_root = os.environ.get(CONFIG_ROOT)
if config_root and not os.path.exists(config_root):
    raise OSError('{}={} does not exist'.format(CONFIG_ROOT, config_root))

pkg_locations = (
    config_root,
)


def get_config_paths(filename=None):
    script_name = os.path.basename(sys.argv[0])

    for dirpath in pkg_locations + (
            os.path.join(sys.prefix, 'config'),
            os.path.join(sys.prefix, 'etc', script_name),
            os.path.expanduser('~/.{}'.format(script_name)),
            ):
        full_path = dirpath

        if filename:
            full_path = os.path.join(full_path, filename)

        yield full_path
