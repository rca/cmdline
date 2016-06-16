from __future__ import absolute_import

# setup logging as close to launching the command as possible
from .logconfig import setup_logging
setup_logging()

from .command import BaseCommand
from .settings import SettingsParser

settings = SettingsParser.get_settings()

__all__ = ['BaseCommand', 'settings']
