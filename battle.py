#! /usr/bin/env python

### USAGE : python battle.py /Users/ilkinulas/robocode ./challengers_config.txt

import sys
import os
import fnmatch
import shutil
import time

ROBOCODE_PATH=sys.argv[1]
ROBOT_REPO_LIST=sys.argv[2]
GIT_CLONE_DIR = ROBOCODE_PATH + "/.robot_repos"
REPO_ROBOT_DELIM = "#"
ROBOT_DELIM = ","
BATTLE_TEMPLATE_REPLACE_STRING = "{{ROBOTS}}"

challengers_config = [line.rstrip('\n') for line in open(ROBOT_REPO_LIST)]
battle_template = open("battle_template.properties", "r").read()

def clone_repos():
    os.system("rm -rf " + GIT_CLONE_DIR)
    os.system("mkdir " + GIT_CLONE_DIR)
    os.chdir(GIT_CLONE_DIR)
    for line in challengers_config:
        os.system("git clone " + line.split(REPO_ROBOT_DELIM)[0])

def build_robots():
    os.chdir(GIT_CLONE_DIR)
    subdirs = [name for name in os.listdir(".") if os.path.isdir(name) and not name.startswith('.')]
    for subdir in subdirs:
        os.chdir(os.path.abspath(subdir))
        os.system("./gradlew clean jar")

def copy_robots():
    os.chdir(GIT_CLONE_DIR)
    jars = []
    for root, dirnames, filenames in os.walk("."):
        for filename in fnmatch.filter(filenames, "*.jar"):
            if "gradle" not in filename:
                jars.append(os.path.join(root, filename))

    for jar in jars:
        shutil.copy(jar, ROBOCODE_PATH+"/robots/")

def prepare_battle_config():
     all_robots = []
     for line in challengers_config:
         robots = line.split(REPO_ROBOT_DELIM)[1].split(ROBOT_DELIM)
         for robot in robots:
             all_robots.append(robot)

     battle_name = time.strftime("%Y%m%d-%H%M%S") + ".battle"
     battle_config = battle_template.replace(BATTLE_TEMPLATE_REPLACE_STRING, ",".join(all_robots))

     battle_file = open(ROBOCODE_PATH + "/battles/" + battle_name, "w")
     battle_file.write(battle_config)
     battle_file.close()
     return battle_name

def run_battle(battle_name):
    os.chdir(ROBOCODE_PATH)
    if not os.path.exists("results"):
        os.makedirs("results")

    command = '''java -Xmx512M -Dsun.io.useCanonCaches=false \
     -cp libs/robocode.jar robocode.Robocode  -nodisplay \
     -battle battles/{{battle}} \
     -results results/{{result}}
    '''

    command = command.replace("{{battle}}", battle_name)
    command = command.replace("{{result}}", battle_name + ".result")
    os.system(command)


if __name__ == '__main__':
    clone_repos()
    build_robots()
    copy_robots()
    battle_name = prepare_battle_config()
    run_battle(battle_name)