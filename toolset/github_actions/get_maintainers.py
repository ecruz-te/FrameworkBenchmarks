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

frameworks = os.getenv("RUN_TESTS")
for framework in frameworks.split(" "):
    _, name = framework.split("/")
    try:
        framework_config = open("frameworks/" + framework + "/benchmark_config.json", "r")
    except FileNotFoundError:
        print("Could not find benchmark_config.json for framework " + framework)
        continue
    maintainers = framework_config.get("maintainers", [])
    if type(maintainers) is str:
        maintainers = [maintainers]
    print("Found maintainers for %s: %s" % (name, maintainers.join(", ")))
exit(0)
