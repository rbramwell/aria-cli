########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
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
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

"""
Handles all commands that start with 'cfy blueprints'
"""

from aria_cli import utils
from aria_cli.logger import get_logger
from aria_cli import messages
from aria_cli.exceptions import CloudifyCliError
from dsl_parser.parser import parse_from_path
from dsl_parser.exceptions import DSLParsingException

SUPPORTED_ARCHIVE_TYPES = ['zip', 'tar', 'tar.gz', 'tar.bz2']


def validate(blueprint_path):
    logger = get_logger()

    logger.info(
        messages.VALIDATING_BLUEPRINT.format(blueprint_path.name))
    try:
        resolver = utils.get_import_resolver()
        parse_from_path(dsl_file_path=blueprint_path.name, resolver=resolver)
    except DSLParsingException as ex:
        msg = (messages.VALIDATING_BLUEPRINT_FAILED
               .format(blueprint_path.name, str(ex)))
        raise CloudifyCliError(msg)
    logger.info(messages.VALIDATING_BLUEPRINT_SUCCEEDED)
