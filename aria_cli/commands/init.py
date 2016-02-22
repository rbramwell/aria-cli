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
Handles 'aria init'
"""

import os
import shutil

from aria_core import constants
from aria_core import exceptions
from aria_core import logger
from aria_core import utils


def init(reset_config, skip_logging=False):
    if os.path.exists(os.path.join(
            os.getcwd(),
            constants.ARIA_WD_SETTINGS_DIRECTORY_NAME,
            constants.ARIA_WD_SETTINGS_FILE_NAME)):
        if not reset_config:
            msg = 'Current directory is already initialized'
            error = exceptions.AriaError(msg)
            error.possible_solutions = [
                "Run 'aria init -b [blueprint-id] -p [path-to-a-blueprint]' "
                "to force re-initialization "
                "(might overwrite existing "
                "configuration files if exist)"
            ]
            raise error
        else:
            shutil.rmtree(os.path.join(
                os.getcwd(),
                constants.ARIA_WD_SETTINGS_DIRECTORY_NAME))

    settings = utils.AriaWorkingDirectorySettings()
    utils.dump_aria_working_dir_settings(settings)
    utils.dump_configuration_file()
    logger.configure_loggers('aria_cli.cli.main')
    if not skip_logging:
        logger.get_logger().info('Initialization completed successfully')
