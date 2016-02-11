########
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
#    * limitations under the License.

"""
Handles 'aria commands'
"""

import json
import shutil
import os


from aria_cli import exceptions
from aria_cli import common
from aria_cli import logger
from aria_cli import utils
from aria_cli.commands import init as aria


from cloudify.workflows import local

from dsl_parser import exceptions as aria_dsl_exceptions
from dsl_parser import parser as aria_dsl_parser

_NAME = 'local'
_STORAGE_DIR_NAME = 'local-storage'


def validate(blueprint_path=None):
    try:
        return aria_dsl_parser.parse_from_path(
            str(blueprint_path)
            if not isinstance(blueprint_path, file)
            else blueprint_path.name)
    except aria_dsl_exceptions.DSLParsingException as e:
        _logger = logger.get_logger()
        _logger.error(str(e))
        raise Exception("Failed to validate blueprint. %s", str(e))


def init(blueprint_path,
         inputs,
         install_plugins_):
    if os.path.isdir(_storage_dir()):
        shutil.rmtree(_storage_dir())

    if not utils.is_initialized():
        aria.init(reset_config=False, skip_logging=True)
    try:
        common.initialize_blueprint(
            blueprint_path=blueprint_path,
            name=_NAME,
            inputs=inputs,
            storage=_storage(),
            install_plugins=install_plugins_,
            resolver=utils.get_import_resolver()
        )
    except ImportError as e:
        e.possible_solutions = [
            "Run 'aria init --install-plugins -p {0}'"
            .format(blueprint_path),
            "Run 'aria install-plugins -p {0}'"
            .format(blueprint_path)
        ]
        raise

    logger.get_logger().info(
        "Initiated {0}\nIf you make changes to the "
        "blueprint, "
        "Run 'aria init -p {0}' "
        "again to apply them"
        .format(blueprint_path))


def execute(workflow_id,
            parameters,
            allow_custom_parameters,
            task_retries,
            task_retry_interval,
            task_thread_pool_size):
    _logger = logger.get_logger()
    parameters = utils.inputs_to_dict(parameters, 'parameters')
    env = _load_env()
    result = env.execute(workflow=workflow_id,
                         parameters=parameters,
                         allow_custom_parameters=allow_custom_parameters,
                         task_retries=task_retries,
                         task_retry_interval=task_retry_interval,
                         task_thread_pool_size=task_thread_pool_size)
    if result is not None:
        _logger.info(json.dumps(result,
                                sort_keys=True,
                                indent=2))


def outputs():
    env = _load_env()
    logger.get_logger().info(
        json.dumps(env.outputs() or {},
                   sort_keys=True,
                   indent=2))


def instances(node_id):
    env = _load_env()
    node_instances = env.storage.get_node_instances()
    if node_id:
        node_instances = [instance for instance in node_instances
                          if instance.node_id == node_id]
        if not node_instances:
            raise exceptions.AriaCliError('No node with id: {0}'
                                          .format(node_id))
    logger.get_logger().info(
        json.dumps(node_instances,
                   sort_keys=True,
                   indent=2))


def install_plugins(blueprint_path):
    common.install_blueprint_plugins(
        blueprint_path=blueprint_path)


def create_requirements(blueprint_path, output):
    if output and os.path.exists(output):
        raise exceptions.AriaCliError('output path already exists : {0}'
                                      .format(output))

    requirements = common.create_requirements(
        blueprint_path=blueprint_path
    )

    if output:
        utils.dump_to_file(requirements, output)
        logger.get_logger().info(
            'Requirements created successfully --> {0}'
            .format(output))
    else:
        # we don't want to use just lgr
        # since we want this output to be prefix free.
        # this will make it possible to pipe the
        # output directly to pip
        for requirement in requirements:
            print(requirement)
            logger.get_logger().info(requirement)


def _storage_dir():
    return os.path.join(utils.get_cwd(), _STORAGE_DIR_NAME)


def _storage():
    return local.FileStorage(storage_dir=_storage_dir())


def _load_env():
    if not os.path.isdir(_storage_dir()):
        error = exceptions.AriaCliError(
            '{0} has not been initialized with a blueprint.'
            .format(utils.get_cwd()))

        # init was probably not executed.
        # suggest solution.

        error.possible_solutions = [
            "Run 'aria init -p [path-to-blueprint]' in this directory"
        ]
        raise error
    return local.load_env(name=_NAME,
                          storage=_storage())
