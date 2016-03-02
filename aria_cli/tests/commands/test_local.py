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
Tests all commands that start with 'aria blueprints'
"""

import os
import json
import tempfile

from aria_cli.tests import cli_runner
from aria_cli.tests.commands import test_cli_command

from aria_core import api
from aria_core.dependencies import futures


class LocalTest(test_cli_command.CliCommandTest):

    def setUp(self):
        super(LocalTest, self).setUp()

    def test_local_init_missing_blueprint_path(self):
        cli_runner.run_cli_expect_system_exit_code(
            'aria init', 2)

    def test_local_init_invalid_blueprint_path(self):
        self._assert_ex(
            'aria init -b idonotexist -p idonotexist.yaml',
            'No such file or directory')

    def test_local_with_multiple_blueprints(self):
        b_id_test_1 = self._local_init(
            custom_blueprint_id='test-1')
        aria_api = api.AriaCoreAPI()
        test_1_env = aria_api.blueprints.load_blueprint_storage(
            b_id_test_1)
        env_path_1 = test_1_env.storage._root_storage_dir
        b_id_test_2 = self._local_init(
            custom_blueprint_id='test-2')
        test_2_env = aria_api.blueprints.load_blueprint_storage(
            b_id_test_2)
        env_path_2 = test_2_env.storage._root_storage_dir
        self.assertTrue(os.path.exists(env_path_1))
        self.assertTrue(os.path.exists(env_path_2))

    def test_local_init(self):
        b_id = self._local_init()
        cli_runner.run_cli(
            'aria outputs -b {0}'.format(b_id))

    def test_local_init_with_inputs(self):
        blueprint_id = self._local_init(
            inputs={'input1': 'new_input1'})
        cli_runner.run_cli(
            'aria outputs -b {0}'.format(blueprint_id))

    def test_local_execute(self):
        blueprint_id = self._local_init()
        self._local_execute(blueprint_id)
        cli_runner.run_cli(
            'aria outputs -b {0}'.format(blueprint_id))

    def test_empty_requirements(self):
        blueprint = 'blueprint_without_plugins'
        blueprint_path = '{0}/local/{1}.yaml'.format(
            test_cli_command.BLUEPRINTS_DIR, blueprint)
        cli_runner.run_cli(
            'aria init --install-plugins -p {0} -b {1}'
            .format(blueprint_path, blueprint))

    def test_local_init_missing_plugin(self):

        blueprint = 'blueprint_with_plugins'
        blueprint_path = '{0}/local/{1}.yaml'.format(
            test_cli_command.BLUEPRINTS_DIR, blueprint)

        expected_possible_solutions = [
            "Run 'aria init --install-plugins -p {0} -b {1}'"
            .format(blueprint_path,
                    blueprint),
        ]
        try:
            self._local_init(blueprint=blueprint)
            self.fail('Excepted ImportError')
        except ImportError as e:
            actual_possible_solutions = e.possible_solutions
            self.assertEqual(actual_possible_solutions,
                             expected_possible_solutions)

    def test_local_execute_with_params(self):
        b_id = self._local_init()
        self._local_execute(b_id,
                            parameters={'param': 'new_param'})
        cli_runner.run_cli(
            'aria outputs -b {0}'.format(b_id))

    def test_local_execute_with_params_allow_custom_false(self):
        b_id = self._local_init()
        self._local_execute(b_id,
                            parameters={
                                'custom_param':
                                    'custom_param_value'},
                            allow_custom=False)

    def test_local_execute_with_params_allow_custom_true(self):
        b_id = self._local_init()
        self._local_execute(b_id,
                            parameters={
                                'custom_param':
                                    'custom_param_value'},
                            allow_custom=True)
        cli_runner.run_cli(
            'aria outputs -b {0}'.format(b_id))

    def test_local_instances(self):
        b_id = self._local_init()
        self._local_execute(b_id)
        cli_runner.run_cli(
            'aria instances -b {0}'.format(b_id))

    def test_local_instances_with_existing_node_id(self):
        b_id = self._local_init()
        self._local_execute(b_id)
        cli_runner.run_cli(
            'aria instances -b {0} --node-id node'.format(b_id))

    def test_execute_with_no_init(self):
        self._assert_ex(
            'aria  execute -w run_test_op_on_nodes -b random-one',
            'Blueprint was not initialized',
            possible_solutions=[
                "Run 'aria init -b [blueprint-id] "
                "-p [path-to-blueprint]' "
                "in this directory"
            ])

    def test_create_requirements(self):

        from aria_cli.tests.resources.blueprints import local

        expected_requirements = {
            'http://localhost/plugin.zip',
            os.path.join(
                os.path.dirname(local.__file__),
                'plugins',
                'local_plugin'),
            'http://localhost/host_plugin.zip'}
        requirements_file_path = os.path.join(
            test_cli_command.TEST_WORK_DIR, 'requirements.txt')

        cli_runner.run_cli('aria create-requirements -p '
                           '{0}/local/blueprint_with_plugins.yaml -o {1}'
                           .format(test_cli_command.BLUEPRINTS_DIR,
                                   requirements_file_path))

        with open(requirements_file_path, 'r') as f:
            actual_requirements = set(f.read().split())
            self.assertEqual(actual_requirements, expected_requirements)

    def test_create_requirements_existing_output_file(self):
        blueprint_path = '{0}/local/blueprint_with_plugins.yaml'.format(
            test_cli_command.BLUEPRINTS_DIR)
        file_path = tempfile.mktemp()
        with open(file_path, 'w') as f:
            f.write('')
        self._assert_ex(
            cli_cmd='aria create-requirements -p {0} -o {1}'
                    .format(blueprint_path, file_path),
            err_str_segment='output path already exists : '
                            '{0}'.format(file_path)
        )

    def test_create_requirements_no_output(self):
        cli_runner.run_cli(
            'aria create-requirements -p '
            '{0}/local/blueprint_with_plugins.yaml'
            .format(test_cli_command.BLUEPRINTS_DIR))

    def _local_init(self,
                    inputs=None,
                    blueprint='blueprint',
                    install_plugins=False,
                    custom_blueprint_id=None):
        b_id = (blueprint if not custom_blueprint_id
                else custom_blueprint_id)
        blueprint_path = '{0}/local/{1}.yaml'.format(
            test_cli_command.BLUEPRINTS_DIR, blueprint)
        flags = '--install-plugins' if install_plugins else ''
        command = 'aria init {0} -b {2} -p {1}'.format(
            flags, blueprint_path, b_id)
        if inputs:
            inputs_path = os.path.join(test_cli_command.TEST_WORK_DIR,
                                       'temp_inputs.json')
            with open(inputs_path, 'w') as f:
                f.write(json.dumps(inputs))
            command = '{0} -i {1}'.format(command, inputs_path)
        cli_runner.run_cli(command)
        return b_id

    def _local_execute(self, blueprint_id,
                       parameters=None,
                       allow_custom=None,
                       workflow_name='run_test_op_on_nodes'):
        if parameters:
            parameters_path = os.path.join(test_cli_command.TEST_WORK_DIR,
                                           'temp_parameters.json')
            with open(parameters_path, 'w') as f:
                f.write(json.dumps(parameters))
            command = 'aria execute -w {0} -p {1} -b {2} '.format(
                workflow_name,
                parameters_path,
                blueprint_id)
            if allow_custom is True:
                cli_runner.run_cli('{0} --allow-custom-parameters'
                                   .format(command))
            elif allow_custom is False:
                self._assert_ex(command, 'does not have the following')
            else:
                cli_runner.run_cli(command)
        else:
            cli_runner.run_cli('aria execute -w {0} -b {1}'
                               .format(workflow_name,
                                       blueprint_id))


@futures.aria_operation
def mock_op(param, custom_param=None, **kwargs):
    props = futures.aria_ctx.instance.runtime_properties
    props['param'] = param
    props['custom_param'] = custom_param
    props['provider_context'] = futures.aria_ctx.provider_context


@futures.aria_workflow
def mock_workflow(param, custom_param=None, **kwargs):
    for node in futures.aria_workflow_ctx.nodes:
        for instance in node.instances:
            instance.execute_operation('test.op', kwargs={
                'param': param,
                'custom_param': custom_param
            })
