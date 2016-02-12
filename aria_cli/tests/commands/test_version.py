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

"""
Tests 'aria --version'
"""

from aria_cli.tests import cli_runner
from aria_cli.tests.commands import test_cli_command


class VersionTest(test_cli_command.CliCommandTest):

    def test_version(self):
        cli_runner.run_cli_expect_system_exit_0('aria --version')
