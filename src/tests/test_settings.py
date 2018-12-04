import unittest
import yaml

from io import StringIO
from unittest import mock

from cmdline import SettingsParser, settings
from cmdline.settings import Settings

from nose.tools import assert_equal

REMOTE_ADDR = """
REMOTE_ADDR:
  default: 'https://example.com/'
  help: the remote address
"""

REMOTE_PORT = """
REMOTE_PORT:
  type: int
  default: '1234'
  help: the remote port
"""

CONFIG_YAML = REMOTE_ADDR
CONFIG_YAML2 = REMOTE_ADDR + REMOTE_PORT
CONFIG_YAML3 = REMOTE_PORT.replace('1234', '5678')

CONFIG_YAML_REQUIRED = """
FOO:
  _positional: true
  help: the foo
"""

CONFIG_YAML_COMMANDS = """
_COMMANDS:
  foo:
    help: the foo
"""


assert_equal(None, settings._compiled_settings)


class SettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        SettingsParser.settings = self.settings

    def test_no_config_found(self, *mocks):
        mocked = mock.Mock()
        mocked.side_effect = [None, None, None]

        self.settings.get_settings_from_file = mocked

        self.assertRaises(Exception, self.settings.run)

    def test_parse(self):
        mocked = mock.Mock()
        mocked.side_effect = [yaml.load(StringIO(CONFIG_YAML)), None, None]

        self.settings.get_settings_from_file = mocked

        self.settings.run()

        self.assertEqual('https://example.com/', self.settings.REMOTE_ADDR)

    def test_overlay_setting_not_in_original(self):
        mocked = mock.Mock()
        mocked.side_effect = [
            yaml.load(StringIO(CONFIG_YAML)),
            None,
            yaml.load(StringIO(CONFIG_YAML2)),
        ]

        self.settings.get_settings_from_file = mocked
        self.settings.paths = ['test']

        self.assertRaises(ValueError, self.settings.run)

    def test_overlay(self):
        mocked = mock.Mock()
        mocked.side_effect = [
            yaml.load(StringIO(CONFIG_YAML2)),
            None,
            yaml.load(StringIO(CONFIG_YAML3)),
        ]

        self.settings.get_settings_from_file = mocked

        self.settings.run()

        self.assertEqual('5678', self.settings.REMOTE_PORT)

    def test_compile_settings(self, *mocks):
        """
        ensure compile settings is only run once
        """
        mocked = mock.Mock()
        mocked.side_effect = [yaml.load(StringIO(CONFIG_YAML)), None, None]

        self.settings.get_settings_from_file = mocked

        settings_run = self.settings.run

        def run():
            return settings_run()

        self.settings.run = mock.Mock(side_effect=run)

        SettingsParser.compile_settings(sys_argv=[])
        SettingsParser.compile_settings(sys_argv=[])

        self.assertEqual(1, len(self.settings.run.mock_calls))

    @mock.patch('argparse.ArgumentParser.exit')
    def test_required(self, *mocks):
        """
        Test a required argument
        """
        mocked = mock.Mock()
        mocked.side_effect = [yaml.load(StringIO(CONFIG_YAML_REQUIRED)), None, None]

        self.settings.get_settings_from_file = mocked

        settings_run = self.settings.run

        self.settings.run = mock.Mock(side_effect=lambda: settings_run())

        SettingsParser.compile_settings(sys_argv=[])

        exit_mock = mocks[0]
        error_message = exit_mock.mock_calls[0][1][1]
        expected = 'the following arguments are required: foo'
        self.assertEqual(True, expected in error_message, '"{}", not in "{}"'.format(expected, error_message))

        self.assertEqual(1, len(self.settings.run.mock_calls))

    def test_subcommand_only_in_commands_entry(self, *mocks):
        mocked = mock.Mock()
        mocked.side_effect = [yaml.load(StringIO(CONFIG_YAML_COMMANDS)), None, None]

        self.settings.get_settings_from_file = mocked

        # process settings files
        self.settings.run()

        # create a parser
        settings_parser = SettingsParser()
        settings_parser.compile_settings(sys_argv=[])

        # ensure the subcommand was created
        self.assertEqual(['foo'], list(settings_parser.subparsers.choices.keys()))

    def test_multiple_subcommands(self, *mocks):
        """
        A single setting can be applied to multiple subcommands
        """
        mocked = mock.Mock()
        settings_yml = """
        FOO:
          type: int
          _subcommand:
            - test1
            - test2
        """
        mocked.side_effect = [yaml.load(settings_yml), None, None]

        self.settings.get_settings_from_file = mocked

        # process settings files
        self.settings.run()

        # create a parser
        settings_parser = SettingsParser()
        settings_parser.compile_settings(sys_argv=[])

        # ensure the subcommand was created
        self.assertEqual(['test1', 'test2'], sorted(list(settings_parser.subparsers.choices.keys())))
