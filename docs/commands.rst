Commands
========

There are two flags that can be used for all operations:
 * ``--verbose`` prints the traceback and prints the events in verbose mode (a full event json)
 * ``--debug`` sets all loggers to debug mode.

Inputs and Parameters
      All commands that accept inputs or paramaters (e.g. "aria execute" ) expect the value to represent a dictionary. Valid formats are:
 * A path to the YAML file
 * A string formatted as YAML
 * A string formatted as "key1=value1;key2=value2"
 
aria
---
.. argparse::
   :module: aria_cli.cli
   :func: register_commands
   :prog: aria
   :path: local