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

from aria_core import exceptions
from aria_core import logger
from aria_core import utils
from aria_core.dependencies import futures

LOG = logger.logging.getLogger(__name__)


def validate(blueprint_path):
    try:
        return futures.aria_dsl_parser.parse_from_path(
            str(blueprint_path)
            if not isinstance(blueprint_path, file)
            else blueprint_path.name)
    except futures.aria_dsl_exceptions.DSLParsingException as e:
        LOG.error(str(e))
        raise Exception("Failed to validate blueprint. %s", str(e))


def init_blueprint_storage(blueprint_id):
    return futures.aria_local.FileStorage(
        storage_dir=utils.storage_dir(blueprint_id))


def load_blueprint_storage_env(blueprint_id):
    if not os.path.isdir(utils.storage_dir(blueprint_id)):
        error = exceptions.AriaError(
            '{0} has not been initialized with a blueprint.'
            .format(utils.get_cwd()))
        error.possible_solutions = [
            ("Run 'aria init -b [blueprint-id] "
             "-p [path-to-blueprint]' in this directory")
        ]
        raise error
    return futures.aria_local.load_env(
        name=blueprint_id,
        storage=init_blueprint_storage(blueprint_id))
