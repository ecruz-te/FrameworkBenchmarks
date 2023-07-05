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
import re
import subprocess

diff_target = os.getenv("TARGET_BRANCH_NAME") 

def fw_found_in_changes(test, changes_output):
    return re.search(
        r"frameworks/" + re.escape(test) + "/",
        changes_output, re.M)

def clean_output(output):
    return os.linesep.join([s for s in output.splitlines() if s])

curr_branch = "HEAD"

changes = clean_output(
    subprocess.check_output([
        'bash', '-c',
        'git --no-pager diff --name-only {0} $(git merge-base {0} {1})'
            .format(curr_branch, diff_target)
    ], text=True))

def get_frameworks(test_lang):
    dir = "frameworks/" + test_lang + "/"
    return [test_lang + "/" + x for x in [x for x in os.listdir(dir) if os.path.isdir(dir + x)]]

test_dirs = []
for frameworks in map(get_frameworks, os.listdir("frameworks")):
    for framework in frameworks:
        test_dirs.append(framework)
affected_frameworks = [fw for fw in test_dirs if fw_found_in_changes(fw, changes)]

maintained_frameworks = {}
unmaintained_frameworks = []

for framework in affected_frameworks:
    _, name = framework.split("/")
    try:
        with open("frameworks/" + framework + "/benchmark_config.json", "r") as framework_config:
            config = json.load(framework_config)
    except FileNotFoundError:
        continue
    framework_maintainers = config.get("maintainers", None)
    if framework_maintainers is None:
        unmaintained_frameworks.append(name)
    else:
        maintained_frameworks[name] = framework_maintainers

if maintained_frameworks:
    print("The following frameworks were affected and have an active list of maintainers pinging maintainers for their input:")
    for framework, maintainers in maintained_frameworks.items():
        print("`%s`: @%s" % (framework, ", @".join(maintainers)))
if unmaintained_frameworks:
    print("The following frameworks were updated, but do not have a list of maintainers:")
    print(" ".join(map(lambda fw: "`%s`" % fw, unmaintained_frameworks)))
exit(0)
