########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############

import argparse
import json
import tempfile
import unittest
import cli_runner

from nose.tools import nottest

from itertools import combinations
from mock import create_autospec
from aria_cli import utils
from aria_cli import commands


TEMP_FILE = tempfile.NamedTemporaryFile()

ARG_VALUES = {
    bool: '',
    int: 1,
    file: TEMP_FILE.name,
    dict: "{\"key\":\"val\"}",
    str: 'mock_value',
    bytearray: 'mock_value1 mock_value2'
}


def get_combinations(command_path):

    def traverse(dictionary, key):
        if 'sub_commands' in dictionary:
            return dictionary['sub_commands'][key]
        return dictionary[key]

    def type_of(arg):
        if 'action' in arg and arg['action'] == 'store_true':
            return bool
        if 'type' in arg:
            if isinstance(arg['type'], argparse.FileType):
                return file
            if arg['type'] == json.loads:
                return dict
        if 'type' not in arg:
            return str
        return arg['type']

    from aria_cli.config.parser_config import parser_config
    parser_conf = parser_config()
    reduced = reduce(traverse, command_path.split(), parser_conf['commands'])
    if 'arguments' not in reduced:
        return []

    required_args = set()
    optional_args = set()
    arguments = reduced['arguments']
    for argument_name, argument in arguments.iteritems():
        possible_arguments = argument_name.split(',')
        type_of_argument = type_of(argument)

        def add_value(arg_name):
            return '{0} {1}'.format(arg_name, ARG_VALUES[type_of_argument])

        if 'required' in argument and argument['required']:
            required_args.update(map(add_value, possible_arguments))
        else:
            optional_args.update(map(add_value, possible_arguments))

    all_commands = []
    for i in range(0, len(optional_args) + 1):
        combs = set(combinations(optional_args, i))
        for combination in combs:
            command = '{0} {1} {2}'.format(
                command_path,
                ' '.join(required_args),
                ' '.join(combination))
            all_commands.append(command)
    return all_commands


def get_all_commands():

    all_commands = []
    from aria_cli.config.parser_config import parser_config
    parser_conf = parser_config()
    for command_name, command in parser_conf['commands'].iteritems():
        if 'sub_commands' in command:
            for sub_command_name in command['sub_commands'].keys():
                command_path = '{0} {1}'.format(command_name, sub_command_name)
                all_commands.append(command_path)
        else:
            all_commands.append(command_name)
    return all_commands


class CliInvocationTest(unittest.TestCase):

    original_blueprints_validate = None
    original_local_init = None
    original_local_execute = None
    original_local_outputs = None
    original_local_instances = None
    original_local_install_plugins = None
    original_local_create_requirements = None

    @classmethod
    def tearDownClass(cls):
        commands.blueprints.validate = cls.original_blueprints_validate
        commands.local.execute = cls.original_local_execute
        commands.local.init = cls.original_local_init
        commands.local.outputs = cls.original_local_outputs
        commands.local.instances = cls.original_local_instances
        commands.local.install_plugins = cls.original_local_install_plugins
        commands.local.create_requirements = cls.original_local_create_requirements  # NOQA

    @classmethod
    def setUpClass(cls):

        # setting up the mocks.
        utils.get_management_server_ip = lambda x: 'localhost'

        # blueprint commands
        cls.original_blueprints_validate = commands.blueprints.validate
        commands.blueprints.validate = create_autospec(
            commands.blueprints.validate, return_value=None
        )

        # local commands
        cls.original_local_init = commands.local.init
        commands.local.init = create_autospec(
            commands.local.init, return_value=None
        )
        cls.original_local_execute = commands.local.execute
        commands.local.execute = create_autospec(
            commands.local.execute, return_value=None
        )
        cls.original_local_outputs = commands.local.outputs
        commands.local.outputs = create_autospec(
            commands.local.outputs, return_value=None
        )
        cls.original_local_instances = commands.local.instances
        commands.local.instances = create_autospec(
            commands.local.instances, return_value=None
        )
        cls.original_local_install_plugins = commands.local.install_plugins
        commands.local.install_plugins = create_autospec(
            commands.local.install_plugins, return_value=None
        )
        cls.original_local_create_requirements = commands.local.create_requirements  # NOQA
        commands.local.create_requirements = create_autospec(
            commands.local.create_requirements, return_value=None
        )

    def _test_all_combinations(self, command_path):
        possible_commands = get_combinations(command_path)
        for command in possible_commands:
            cli_runner.run_cli('cfy {0}'.format(command))

    @nottest
    # excluded these tests since the number of possible parameters
    # combinations has grown too large. need to change these tests so that
    # they'll be linear and not exponential in the number of optional
    # parameters for a given command.
    def test_all_commands(self):

        """
        Run all commands.
        """

        all_commands = get_all_commands()
        for command in all_commands:
            possible_commands = get_combinations(command)
            for possible_command in possible_commands:
                cli_runner.run_cli('cfy {0}'.format(possible_command))

    @nottest
    def test_all_commands_help(self):

        """
        Run all commands with 'help' flags.
        """

        all_commands = get_all_commands()
        for command in all_commands:
            cli_runner.run_cli_expect_system_exit_0(
                'cfy {0} -h'.format(command)
            )
            cli_runner.run_cli_expect_system_exit_0(
                'cfy {0} --help'.format(command)
            )

    @nottest
    def test_all_commands_verbose(self):

        """
        Run all commands with 'verbosity' flags.
        """

        all_commands = get_all_commands()
        for command in all_commands:
            possible_commands = get_combinations(command)
            for possible_command in possible_commands:
                cli_runner.run_cli(
                    'cfy {0} -v'.format(possible_command)
                )
                cli_runner.run_cli(
                    'cfy {0} --verbose'.format(possible_command)
                )
