# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import os
import shutil
import unittest
from mock import patch


from aria_cli import exceptions
from aria_cli import utils
from aria_cli.dependencies import futures
from aria_cli.tests import cli_runner

TEST_DIR = '/tmp/aria-cli-component-tests'
TEST_WORK_DIR = TEST_DIR + "/aria"
THIS_DIR = os.path.dirname(os.path.dirname(__file__))
BLUEPRINTS_DIR = os.path.join(
    THIS_DIR, 'resources', 'blueprints')


class CliCommandTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = futures.aria_side_utils.setup_logger(
            'CliCommandTest')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_DIR)

    def setUp(self):
        logdir = os.path.dirname(utils.DEFAULT_LOG_FILE)

        # create log folder
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        # create test working directory
        if not os.path.exists(TEST_WORK_DIR):
            os.makedirs(TEST_WORK_DIR)

        self.original_utils_get_cwd = utils.get_cwd
        utils.get_cwd = lambda: TEST_WORK_DIR
        self.original_utils_os_getcwd = os.getcwd
        os.getcwd = lambda: TEST_WORK_DIR

    def tearDown(self):

        # remove mocks
        utils.get_cwd = self.original_utils_get_cwd = utils.get_cwd
        os.getcwd = self.original_utils_os_getcwd = os.getcwd

        # empty log file
        if os.path.exists(utils.DEFAULT_LOG_FILE):
            with open(utils.DEFAULT_LOG_FILE, 'w') as f:
                f.write('')

        # delete test working directory
        if os.path.exists(TEST_WORK_DIR):
            shutil.rmtree(TEST_WORK_DIR)

    def _assert_ex(self,
                   cli_cmd,
                   err_str_segment,
                   possible_solutions=None):

        def _assert():
            self.assertIn(err_str_segment, str(ex))
            if possible_solutions:
                if hasattr(ex, 'possible_solutions'):
                    self.assertEqual(ex.possible_solutions,
                                     possible_solutions)
                else:
                    self.fail('Exception should have '
                              'declared possible solutions')

        try:
            cli_runner.run_cli(cli_cmd)
            self.fail('Expected error {0} was not raised for command {1}'
                      .format(err_str_segment, cli_cmd))
        except (exceptions.AriaCliError,
                SystemExit,
                exceptions.AriaValidationError,
                ValueError,
                IOError,
                ImportError,
                Exception) as ex:
            _assert()

    def assert_method_called(self,
                             cli_command,
                             module,
                             function_name,
                             kwargs):
        with patch.object(module, function_name) as mock:
            try:
                cli_runner.run_cli(cli_command)
            except BaseException as e:
                self.logger.info(e.message)
            mock.assert_called_with(**kwargs)

    def _create_cosmo_wd_settings(self, settings=None):
        directory_settings = utils.AriaWorkingDirectorySettings()
        directory_settings.set_management_server('localhost')
        utils.delete_cloudify_working_dir_settings()
        utils.dump_aria_working_dir_settings(
            settings or directory_settings, update=False)
        utils.dump_configuration_file()

    def _read_cosmo_wd_settings(self):
        return utils.load_aria_working_dir_settings()
