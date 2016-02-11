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

# flake8: noqa

import argparse

from aria_cli import commands as aria
from aria_cli.config import argument_utils

from argcomplete.completers import FilesCompleter

yaml_files_completer = FilesCompleter(['*.yml', '*.yaml'])
archive_files_completer = FilesCompleter(
    ['*.zip', '*.tar', '*.tar.gz', '*.tar.bz2'])

FORMAT_INPUT_AS_YAML_OR_DICT = 'formatted as YAML or as "key1=value1;key2=value2"'


def workflow_id_argument(hlp):
    return {
        'metavar': 'WORKFLOW',
        'dest': 'workflow_id',
        'type': str,
        'required': True,
        'help': hlp,
    }


def parser_config():
    return {
        'description': 'Manages ARIA in different Cloud Environments',
        'arguments': {
            '--version': {
                'help': 'show version information and exit',
                'action': aria.version
            }
        },
        'commands': {
            'validate': {
                'arguments': {
                    '-p,--blueprint-path': {
                        'metavar': 'BLUEPRINT_FILE',
                        'type': argparse.FileType(),
                        'dest': 'blueprint_path',
                        'required': True,
                        'help': "Path to the application's blueprint file",
                        'completer': yaml_files_completer
                    }
                },
                'help': 'command for validating a blueprint',
                'handler': aria.local.validate
            },
            'init': {
                'help': 'Init a local workflow execution environment in '
                        'in the current working directory',
                'arguments': {
                    '-p,--blueprint-path': {
                        'dest': 'blueprint_path',
                        'metavar': 'BLUEPRINT_PATH',
                        'type': str,
                        'required': True,
                        'help': 'Path to a blueprint'
                    },
                    '-i,--inputs': {
                        'metavar': 'INPUTS',
                        'dest': 'inputs',
                        'required': False,
                        'help': 'Inputs file/string for the local workflow creation ({0})'
                                .format(FORMAT_INPUT_AS_YAML_OR_DICT)
                    },
                    '--install-plugins': {
                        'dest': 'install_plugins_',
                        'action': 'store_true',
                        'default': False,
                        'help': 'Install necessary plugins of the given blueprint.'
                    }
                },
                'handler': aria.local.init
            },
            'install-plugins': {
                'help': 'Installs the necessary plugins for a given blueprint',
                'arguments': {
                    '-p,--blueprint-path': {
                        'dest': 'blueprint_path',
                        'metavar': 'BLUEPRINT_PATH',
                        'type': str,
                        'required': True,
                        'help': 'Path to a blueprint'
                    }
                },
                'handler': aria.local.install_plugins
            },
            'create-requirements': {
                'help': 'Creates a PIP compliant requirements file for the given blueprint',
                'arguments': {
                    '-p,--blueprint-path': {
                        'dest': 'blueprint_path',
                        'metavar': 'BLUEPRINT_PATH',
                        'type': str,
                        'required': True,
                        'help': 'Path to a blueprint'
                    },
                    '-o,--output': {
                        'metavar': 'REQUIREMENTS_OUTPUT',
                        'dest': 'output',
                        'required': False,
                        'help': 'Path to a file that will hold the '
                                'requirements of the blueprint'
                    }
                },
                'handler': aria.local.create_requirements
            },
            'execute': {
                'help': 'Execute a workflow locally',
                'arguments': {
                    '-w,--workflow':
                        argument_utils.remove_completer(
                            workflow_id_argument(
                                hlp='The workflow to execute locally')),
                    '-p,--parameters': {
                        'metavar': 'PARAMETERS',
                        'dest': 'parameters',
                        'default': {},
                        'type': str,
                        'required': False,
                        'help': 'Parameters for the workflow execution ({0})'
                                .format(FORMAT_INPUT_AS_YAML_OR_DICT)
                    },
                    '--allow-custom-parameters': {
                        'dest': 'allow_custom_parameters',
                        'action': 'store_true',
                        'default': False,
                        'help': 'A flag for allowing the passing of custom parameters ('
                                "parameters which were not defined in the workflow's schema in "
                                'the blueprint) to the execution'
                    },
                    '--task-retries': {
                        'metavar': 'TASK_RETRIES',
                        'dest': 'task_retries',
                        'default': 0,
                        'type': int,
                        'help': 'How many times should a task be retried in case '
                                'it fails'
                    },
                    '--task-retry-interval': {
                        'metavar': 'TASK_RETRY_INTERVAL',
                        'dest': 'task_retry_interval',
                        'default': 1,
                        'type': int,
                        'help': 'How many seconds to wait before each task is retried'
                    },
                    '--task-thread-pool-size': {
                        'metavar': 'TASK_THREAD_POOL_SIZE',
                        'dest': 'task_thread_pool_size',
                        'default': 1,
                        'type': int,
                        'help': 'The size of the thread pool size to execute tasks in'
                    }
                },
                'handler': aria.local.execute
            },
            'outputs': {
                'help': 'Display outputs',
                'arguments': {},
                'handler': aria.local.outputs
            },
            'instances': {
                'help': 'Display node instances',
                'arguments': {
                    '--node-id': {
                        'metavar': 'NODE_ID',
                        'dest': 'node_id',
                        'default': None,
                        'type': str,
                        'required': False,
                        'help': 'Only display node instances of this node id'
                    }
                },
                'handler': aria.local.instances
            }
        }
    }
