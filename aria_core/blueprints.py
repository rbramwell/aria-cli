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

from aria_core import logger
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
