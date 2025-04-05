from argparse import ArgumentParser
from pathlib import Path
import src.color as color
import sys
import json
import os
import shutil

# Global files  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

GLOBAL_DIR = Path(sys.argv[0])
TEMPLATES_DIR = GLOBAL_DIR / 'templates'
DEBUG_TEMPLATE_DIR = TEMPLATES_DIR / '.debug'
ENVIRONMENT_TEMPLATE_DIR = TEMPLATES_DIR / 'environment'


# Working files = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# These are relative to './'


WORKING_DIR = Path(".debug")
SETTINGS_FILE = WORKING_DIR / "settings.json"


# Environment files = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# These are relative to '.debug/<enviroment>'


SCRIPTS_DIR = Path("scripts")
TESTING_DIR = Path("testing")
TESTS_DIR = Path("tests")

RUN_SCRIPT = SCRIPTS_DIR / "run"
GENERATE_SCRIPT = SCRIPTS_DIR / "generate"
COMPILE_SCRIPT = SCRIPTS_DIR / "compile"
CHECK_SCRIPT = SCRIPTS_DIR / "check"

# Global scripts  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


DEFAULT_SETTINGS = {
    "current": None,
    "all": []
}

def get_setting(key):
    try:
        with open(SETTINGS_FILE) as settings:
            return json.load(settings)[key]
    except FileNotFoundError:
        color.print_error(f"No file '{SETTINGS_FILE}' found")
    except PermissionError:
        color.print_error(f"No permissions to read '{SETTINGS_FILE}' file")
    except OSError:
        color.print_error(f"Error occured while reading '{SETTINGS_FILE}' file")

def set_setting(key, value):
    try:
        with open(SETTINGS_FILE) as settings:
            d = json.load(settings)
    except FileNotFoundError:
        color.print_error(f"No file '{SETTINGS_FILE}' found")
    except PermissionError:
        color.print_error(f"No permissions to read '{SETTINGS_FILE}' file")
    except OSError:
        color.print_error(f"Error occured while reading '{SETTINGS_FILE}' file")
        
    d[key] = value
    try:
        with open(SETTINGS_FILE, 'w') as settings:
            json.dump(d, settings, indent=4)
    except PermissionError:
        color.print_error(f"No permissions to write '{SETTINGS_FILE}' file")
    except OSError:
        color.print_error(f"Error occured while writing to '{SETTINGS_FILE}' file")

def init_global():
    if (not os.path.isdir(WORKING_DIR)):
        shutil.copytree(DEBUG_TEMPLATE_DIR, WORKING_DIR)


# Commands  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


def init(parsed: ArgumentParser):
    init_global()
    try:
        shutil.copytree(ENVIRONMENT_TEMPLATE_DIR, WORKING_DIR / parsed.name)
    except FileExistsError:
        color.print_error(f"Environment '{parsed.name}' already exists")
    except FileNotFoundError:
        color.print_error("Incorrect name of the environment")

def remove(parsed: ArgumentParser):
    all_env = get_setting('all')
    if parsed.name not in all_env:
        color.print_error(f"No environment with name '{parsed.name}' found in cwd. Run 'debug show --all' to show the list of all available environments")
    try:
        shutil.rmtree(WORKING_DIR / parsed.name)
        all_env.remove(parsed.name)
        set_setting('all', all_env)
        set_setting('current', None)
        
    except OSError:
        color.print_error(f"An error occured. Sorry :(")

def show(parsed: ArgumentParser):
    if parsed.current:
        if get_setting('current') is not None:
            color.print_info(f"On environment '{get_setting('current')}'")
        else:
            color.print_warning('You are now not switched to any of the environments')
    if parsed.all:
        print(*get_setting('all'), sep='\n')

def switch(parsed: ArgumentParser):
    if parsed.name in get_setting('all'):
        if parsed.name == get_setting('current'):
            color.print_info(f"Already on '{parsed.name}'", 0)
        set_setting('current', parsed.name)
    else:
        color.print_error(f"No environment with name '{parsed.name}' found in cwd. Run 'debug show --all' to show the list of all available environments")

def generate(parsed: ArgumentParser):
    current_env = get_setting('current')
    