#!/usr/bin/env python

# @file:        toolset/github_actions/get_maintainers.py
# @author:      Elwyn Cruz (ecruz-te)
#
# @description: This script is only for use within Github Actions. It is meant
# to get a list of maintainers to ping for a PR whenever their framework
# is updated.
# This script is meant to be used in conjunction with the github_actions_diff.py
# to determine which frameworks have been updated.

import os
import json

frameworks = os.getenv("RUN_TESTS")
maintained_frameworks = {}
unmaintained_frameworks = []
for framework in frameworks.split(" "):
    _, name = framework.split("/")
    try:
        with open("frameworks/" + framework + "/benchmark_config.json", "r") as framework_config:
            config = json.load(framework_config)
    except FileNotFoundError:
        print("Could not find benchmark_config.json for framework " + framework)
        continue
    framework_maintainers = config.get("maintainers", None)
    if framework_maintainers is None:
        unmaintained_frameworks += name
    else:
        maintained_frameworks[name] = framework_maintainers
if maintained_frameworks is not None:
    print("This PR contains updates to the following frameworks, pinging maintainers for their input:")
    for framework, maintainers in maintained_frameworks.items():
        print("%s: %s" % (name, ", ".join(maintainers)))
if unmaintained_frameworks:
    print("The following frameworks did not have their maintainers listed in `benchmark_config.json`:")
    for framework in unmaintained_frameworks:
        print(framework)
exit(0)
