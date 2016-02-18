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


import tempfile

from aria_core import constants
from aria_core import exceptions
from aria_core import logger
from aria_core import logger_config
from aria_core import utils
from aria_core.dependencies import futures

from aria_processor import blueprint_processor

LOG = logger.get_logger('aria_cli.cli.main')


def initialize_blueprint(blueprint_path,
                         name,
                         storage,
                         install_plugins=False,
                         inputs=None,
                         resolver=None):
    if install_plugins:
        install_blueprint_plugins(
            blueprint_path=blueprint_path)
    provider_context = (
        logger_config.AriaConfig().local_provider_context)
    inputs = utils.inputs_to_dict(inputs, 'inputs')
    return futures.aria_local.init_env(
        blueprint_path=blueprint_path,
        name=name,
        inputs=inputs,
        storage=storage,
        ignored_modules=constants.IGNORED_LOCAL_WORKFLOW_MODULES,
        provider_context=provider_context,
        resolver=resolver)


def install_blueprint_plugins(blueprint_path, logger_instance=None):

    requirements = blueprint_processor.create_requirements(
        blueprint_path=blueprint_path
    )

    if requirements:
        # validate we are inside a virtual env
        if not utils.is_virtual_env():
            raise exceptions.AriaError(
                'You must be running inside a '
                'virtualenv to install blueprint plugins')

        runner = futures.aria_side_utils.LocalCommandRunner(LOG)
        # dump the requirements to a file
        # and let pip install it.
        # this will utilize pip's mechanism
        # of cleanup in case an installation fails.
        tmp_path = tempfile.mkstemp(suffix='.txt', prefix='requirements_')[1]
        utils.dump_to_file(collection=requirements, file_path=tmp_path)
        runner.run(command='pip install -r {0}'.format(tmp_path),
                   stdout_pipe=False)
    else:
        LOG.debug('There are no plugins to install.')
