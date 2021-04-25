#!/usr/bin/env python3

from aws_cdk import core
from cdk_stacks.scraper_stack import ScraperStack
import json

with open('configs.json') as f:
  configs = json.load(f)

app = core.App()
#configs = configs[app.node.try_get_context("stage")]

ScraperStack(app, "scraper-dev", configs['dev'])
ScraperStack(app, "scraper-prod", configs['prod'])

app.synth()
