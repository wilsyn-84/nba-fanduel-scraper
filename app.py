#!/usr/bin/env python3

from aws_cdk import core
from cdk_stacks.scrapper_stack import ScrapperStack
import json

with open('configs.json') as f:
  configs = json.load(f)

app = core.App()
configs = configs[app.node.try_get_context("stage")]
ScrapperStack(app, "scrapper", configs)

app.synth()
