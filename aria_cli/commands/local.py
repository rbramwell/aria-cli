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
Handles 'aria commands'
"""

import json
import shutil
import os


from aria_cli.commands import init as aria_cli

from aria_cli import messages
from aria_core import api
from aria_core import exceptions
from aria_core import utils
from aria_core import logger


LOG = logger.get_logger('aria_cli.cli.main')


def validate(blueprint_path=None):
    LOG.info(messages.VALIDATING_BLUEPRINT)
    aria_api = api.AriaCoreAPI()
    aria_api.blueprints.validate(blueprint_path.name)
    LOG.info(messages.VALIDATING_BLUEPRINT_SUCCEEDED)


def init(blueprint_id,
         blueprint_path,
         inputs,
         install_plugins_):

    aria_api = api.AriaCoreAPI()
    if os.path.isdir(utils.storage_dir(blueprint_id)):
        shutil.rmtree(utils.storage_dir(blueprint_id))

    if not utils.is_initialized():
        aria_cli.init(reset_config=False, skip_logging=True)

    try:
        aria_api.blueprints.initialize(
            blueprint_id,
            blueprint_path,
            inputs=inputs,
            install_plugins=install_plugins_,
        )
    except BaseException as e:
        e.possible_solutions = [
            "Run 'aria init --install-plugins -p {0} -b {1}'"
            .format(blueprint_path,
                    blueprint_id)
        ]
        LOG.exception(e)
        raise e

    LOG.info(
        "Initiated {0}\nIf you make changes to the "
        "blueprint, "
        "Run 'aria init -b {1} -p {0}' "
        "again to apply them"
        .format(blueprint_path, blueprint_id))


def _validate_and_load_env(blueprint_id):
    if not os.path.isdir(utils.storage_dir(blueprint_id)):
        error = exceptions.AriaError(
            '{0} has not been initialized with a blueprint.'
            .format(utils.get_cwd()))
        error.possible_solutions = [
            ("Run 'aria init -b [blueprint-id] "
             "-p [path-to-blueprint]' in this directory")
        ]
        raise error
    aria_api = api.AriaCoreAPI()
    return aria_api.blueprints.load_blueprint_storage(
        blueprint_id)


def execute(blueprint_id,
            workflow_id,
            parameters,
            allow_custom_parameters,
            task_retries,
            task_retry_interval):
    aria_api = api.AriaCoreAPI()
    try:
        aria_api.blueprints.load_blueprint_storage(blueprint_id)
    except Exception:
        e = exceptions.AriaError(
            "Blueprint was not initialized.")
        e.possible_solutions = [
            "Run 'aria init -b [blueprint-id] "
            "-p [path-to-blueprint]' "
            "in this directory"
        ]
        raise e
    parameters = utils.inputs_to_dict(parameters, 'parameters')
    result = aria_api.executions.execute_custom(
        blueprint_id,
        workflow_id,
        parameters=parameters,
        allow_custom_parameters=allow_custom_parameters,
        task_retries=task_retries,
        task_retry_interval=task_retry_interval)
    if result:
        LOG.info(json.dumps(result,
                            sort_keys=True,
                            indent=2))


def outputs(blueprint_id):
    aria_api = api.AriaCoreAPI()
    _outputs = aria_api.blueprints.outputs(blueprint_id)
    LOG.info(_outputs)


def instances(blueprint_id, node_id):
    aria_api = api.AriaCoreAPI()
    node_instances = aria_api.blueprints.instances(
        blueprint_id, node_id=node_id)
    LOG.info(
        json.dumps(node_instances,
                   sort_keys=True,
                   indent=2))


def create_requirements(blueprint_path, output):
    if output and os.path.exists(output):
        raise exceptions.AriaError('output path already exists : {0}'
                                   .format(output))
    aria_api = api.AriaCoreAPI()
    requirements = aria_api.blueprints.create_requirements(
        blueprint_path=blueprint_path
    )

    if output:
        utils.dump_to_file(requirements, output)
        LOG.info(
            'Requirements created successfully --> {0}'
            .format(output))
    else:
        for requirement in requirements:
            LOG.info(requirement)
