# ARIA CLI

* Master Branch [![Build Status](https://travis-ci.org/aria-tosca/aria-cli.svg?branch=master)](https://travis-ci.org/aria-tosca/aria-cli)
* PyPI [![PyPI](http://img.shields.io/pypi/dm/aria-tosca.svg)](http://img.shields.io/pypi/dm/aria-tosca.svg)
* Version [![PypI](http://img.shields.io/pypi/v/aria-tosca.svg)](http://img.shields.io/pypi/v/aria-tosca.svg)

ARIA is an Open Source implementation of TOSCA, that allows you to orchestrate applications on any cloud platform.

See [TOSCA](http://docs.oasis-open.org/tosca/TOSCA/v1.0/os/TOSCA-v1.0-os.html)

ARIA's Command Line Interface.

## Setup

`pip install aria-tosca`

## Usage

* Write/Download a TOSCA blueprint - See https://github.com/aria-tosca/aria-examples

* Get blueprint requirements:

 `aria create-requirements -p blueprint.yaml`

* Initialze aria with TOSCA blueprint:

 `aria validate -p blueprint.yaml`
 `aria init -b blueprint-id -p blueprint.yaml -i inputs.yaml --install-plugins --debug`

* Install the blueprint:

  `aria execute -w install -b blueprint-id --allow-custom-parameters --task-retries 10 --task-retry-interval 10`

* See blueprint deployment outputs:

  `aria outputs -b blueprint-id`

* See blueprint deployment outputs:

  `aria instances -b blueprint-id`

or

  `aria instances -b blueprint-id --node-id node-id`


## Read more

See [ARIA CLI](http://aria-cli.readthedocs.org/en/latest/)
