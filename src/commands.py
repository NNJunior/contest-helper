from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen, PIPE, TimeoutExpired
from shlex import quote
import time
import src.color as color
import src.testing as testing
import sys
import json
import os
import shutil

TEXT_EDITOR = 'nano'

# Global files  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


GLOBAL_DIR = Path(sys.argv[0])
TEMPLATES_DIR = GLOBAL_DIR / 'templates'
DEBUG_TEMPLATE_DIR = TEMPLATES_DIR / '.debug'
ENVIRONMENT_TEMPLATE_DIR = TEMPLATES_DIR / 'environment'


# Working files = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# These are relative to './'


WORKING_DIR = Path(".debug")
ENVIRONMENT_DIR = None
SETTINGS_FILE = WORKING_DIR / "settings.json"


# Global scripts  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


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

def init():
    if (not os.path.isdir(WORKING_DIR)):
        shutil.copytree(DEBUG_TEMPLATE_DIR, WORKING_DIR)

if os.path.isfile(SETTINGS_FILE) and get_setting('current') is not None:
    ENVIRONMENT_DIR = WORKING_DIR / get_setting('current')


# Environment files = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# These are relative to '.debug/<current enviroment>'


SCRIPTS_DIR = None if ENVIRONMENT_DIR is None else ENVIRONMENT_DIR / "scripts"

RUN_SCRIPT      = None if SCRIPTS_DIR is None else SCRIPTS_DIR / "run"
GENERATE_SCRIPT = None if SCRIPTS_DIR is None else SCRIPTS_DIR / "generate"
COMPILE_SCRIPT  = None if SCRIPTS_DIR is None else SCRIPTS_DIR / "compile"
CHECK_SCRIPT    = None if SCRIPTS_DIR is None else SCRIPTS_DIR / "check"

TESTING_DIR = None if ENVIRONMENT_DIR is None else ENVIRONMENT_DIR / "testing"

INPUT_FILE  = None if TESTING_DIR is None else TESTING_DIR / "input.txt"
OUTPUT_FILE = None if TESTING_DIR is None else TESTING_DIR / "output.txt"
ERRORS_FILE = None if TESTING_DIR is None else TESTING_DIR / "errors.txt"

TESTS_DIR   = None if ENVIRONMENT_DIR is None else ENVIRONMENT_DIR / "tests"


# Commands  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


def new(parsed: ArgumentParser):
    init()
    try:
        shutil.copytree(ENVIRONMENT_TEMPLATE_DIR, WORKING_DIR / parsed.name)
        set_setting('all', get_setting('all') + [parsed.name])
        set_setting('current', parsed.name)
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
        color.print_error(f"An unknowed error occured. Sorry :(")

def show(parsed: ArgumentParser):
    if parsed.current:
        if ENVIRONMENT_DIR.name is not None:
            color.print_info(f"In environment '{ENVIRONMENT_DIR.name}'")
        else:
            color.print_warning('You are now not inside any of the environments')
    if parsed.all:
        print(*get_setting('all'), sep='\n')

def switch(parsed: ArgumentParser):
    if parsed.name in get_setting('all'):
        if parsed.name == ENVIRONMENT_DIR.name:
            color.print_info(f"Already on '{parsed.name}'", exit_code=0)
        set_setting('current', parsed.name)
    else:
        color.print_error(f"No environment with name '{parsed.name}' found in cwd. Run 'debug show --all' to show the list of all available environments")

def generate(parsed: ArgumentParser):
    if ENVIRONMENT_DIR is None:
        color.print_error('You are now not inside any of the environments')
    try:
        shutil.rmtree(TESTS_DIR)
    except FileNotFoundError:
        pass
    except OSError:
        color.print_error(f"An unknown error occured. Sorry :(")
    
    os.mkdir(TESTS_DIR)
    for index in range(parsed.amount):
        try:
            gen_process = Popen([quote(str(GENERATE_SCRIPT.absolute()))], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = gen_process.communicate()
            if gen_process.returncode == 0:
                with open(TESTS_DIR / testing.test_name(index), 'wb') as writer:
                    writer.write(stdout)
                    color.print_info(f"Generated: {testing.test_name(index)}")
            else:
                raise OSError(stderr.decode())
        except OSError as e:
            color.print_error(f"An error occured while generating {testing.test_name(index)}:", *e.args, exit_code=None)
            index += 1

def compile(parsed: ArgumentParser):
    if ENVIRONMENT_DIR is None:
        color.print_error('You are now not inside any of the environments')
    compile_process = Popen([quote(str(COMPILE_SCRIPT.absolute()))], shell=True, cwd=TESTING_DIR)
    color.print_info('Compiling...')
    compile_process.wait()
    if compile_process.returncode == 0:
        color.print_info('Compilation successfull!')
    else:
        sys.exit(1)

def run(parsed: ArgumentParser):
    if ENVIRONMENT_DIR is None:
        color.print_error('You are now not inside any of the environments')
    
    def run_test(path_to_test):
        try:
            shutil.copy(path_to_test, INPUT_FILE)
        except:
            color.print_error(f"Cannot copy {path_to_test} to {INPUT_FILE}", None)
            return None
        
        stdin = open(INPUT_FILE, 'rb')
        stdout = open(OUTPUT_FILE, 'wb')
        stderr = open(ERRORS_FILE, 'wb')
        tstart = time.time()
        run_process = Popen(
            [quote(str(RUN_SCRIPT.absolute()))],
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,            
            shell=True,
            cwd=TESTING_DIR
        )
        stderr.close()
        stdout.close()
        stdin.close()
        
        time_total = None
        
        try:
            run_process.wait(parsed.timeout)
        except TimeoutExpired as e:
            run_process.kill()
        tend = time.time()
        time_total = tend - tstart
        
        stdin = open(INPUT_FILE, 'rb')
        check_process = Popen(
            [quote(str(CHECK_SCRIPT.absolute()))],
            stdin=stdin,
            stdout=PIPE,
            stderr=PIPE,            
            shell=True,
            cwd=TESTING_DIR
        )
        stdin.close()
        checker_output, checker_errors = check_process.communicate()
        
        testing.print_test_info(
            path_to_test.name,
            testing.status(
                run_process.returncode,
                check_process.returncode,
                time_total,
                parsed.timeout
            ),
            time_total
        )
        if parsed.input:
            with open(INPUT_FILE) as reader:
                testing.print_additional_data('input.txt:', reader.read())
        if parsed.output:
            with open(OUTPUT_FILE) as reader:
                testing.print_additional_data('output.txt:', reader.read())
        if parsed.errors:
            color.mark_warning()
            with open(ERRORS_FILE) as reader:
                testing.print_additional_data('errors.txt:', reader.read())
        if parsed.checker_output:
            testing.print_additional_data('checker output:', checker_output.decode())
        if parsed.checker_errors:
            testing.print_additional_data('checker errors:', checker_errors.decode())
    if not parsed.no_compile:
        compile(None)
    
    if parsed.inf:
        pass
    tests = parsed.tests
    if parsed.all:
        try:
            tests = sorted(os.listdir(TESTS_DIR), key=testing.index_from_test)
        except FileNotFoundError:
            color.print_error(f"Folder '{TESTS_DIR}' not found")
        except PermissionError:
            color.print_error(f"No permissions to read '{TESTS_DIR}' folder")
        except OSError:
            color.print_error(f"Error occured while accessing '{TESTS_DIR}' folder")
    
    color.print_info('Running tests...')
    for test in tests:
        try:
            run_test(TESTS_DIR / test)
        except OSError:
            color.print_error(f"An unknown error occured while executing '{test}'")

def configure(parsed: ArgumentParser):
    match parsed.script:
        case 'run':
            p = Popen([TEXT_EDITOR, RUN_SCRIPT])
        case 'gen':
            p = Popen([TEXT_EDITOR, GENERATE_SCRIPT])
        case 'compile':
            p = Popen([TEXT_EDITOR, COMPILE_SCRIPT])
        case 'check':
            p = Popen([TEXT_EDITOR, CHECK_SCRIPT])
    
    p.wait()