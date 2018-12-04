import os
import unittest

from unittest import mock

from cmdline.config import get_config_paths


@mock.patch('cmdline.config.os')
@mock.patch('cmdline.config.sys')
class ConfigTestCase(unittest.TestCase):
    def test_get_config_paths(self, *mocks):
        """
        ensure config paths are processed
        """
        os.environ['HOME'] = '/home/user'

        sys_mock = mocks[-2]
        sys_mock.argv = ['script_name']
        sys_mock.prefix = '/foo'

        os_mock = mocks[-1]
        os_mock.environ = {}
        os_mock.path = os.path

        expected = [
            '/foo/cmdline/unittest',
            '/foo/etc/script_name',
            '/home/user/.script_name'
        ]

        self.assertEqual(expected, list(get_config_paths()))

    def test_config_root_env(self, *mocks):
        """
        ensure CMDLINE_CONFIG_ROOT is prepended to config paths
        """
        the_path = '/the/path'

        os_mock = mocks[-1]
        os_mock.environ = {
            'CMDLINE_CONFIG_ROOT': the_path,
        }

        config_paths = list(get_config_paths())

        self.assertEqual(the_path, config_paths[-1])

    def test_config_root_env_reversed(self, *mocks):
        """
        ensure CMDLINE_CONFIG_ROOT is prepended to config paths
        """
        the_path = '/the/path'

        os_mock = mocks[-1]
        os_mock.environ = {
            'CMDLINE_CONFIG_ROOT': the_path,
        }

        config_paths = list(get_config_paths(reversed=True))

        self.assertEqual(the_path, config_paths[0])

    def test_get_config_paths_with_filename(self, *mocks):
        """
        ensure given filename is appended to paths
        """
        os.environ['HOME'] = '/home/user'

        sys_mock = mocks[-2]
        sys_mock.argv = ['script_name']
        sys_mock.prefix = '/foo'

        os_mock = mocks[-1]
        os_mock.environ = {}
        os_mock.path = os.path

        expected = [
            '/foo/cmdline/unittest/filename',
            '/foo/etc/script_name/filename',
            '/home/user/.script_name/filename',
        ]

        self.assertEqual(expected, list(get_config_paths('filename')))
