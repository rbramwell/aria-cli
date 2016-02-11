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

ARIA_WD_SETTINGS_FILE_NAME = 'context'
ARIA_WD_SETTINGS_DIRECTORY_NAME = '.aria'
CONFIG_FILE_NAME = 'aria-config.yaml'
DEFAULTS_CONFIG_FILE_NAME = 'aria-config.defaults.yaml'

WORKFLOW_TASK_RETRIES = -1
WORKFLOW_TASK_RETRY_INTERVAL = 30

POLICY_ENGINE_START_TIMEOUT = 30

DEFAULT_REST_PORT = 80
SECURED_REST_PORT = 443
DEFAULT_PROTOCOL = 'http'
SECURED_PROTOCOL = 'https'

IGNORED_LOCAL_WORKFLOW_MODULES = (
    'cloudify_agent.operations',
    'cloudify_agent.installer.operations',
    'worker_installer.tasks',
    'plugin_installer.tasks',
    'windows_agent_installer.tasks',
    'windows_plugin_installer.tasks',
)

BASIC_AUTH_PREFIX = 'Basic'

API_VERSION = 'v2'
