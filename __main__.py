import argparse
import src.commands as commands
from src.config import VERSION
import sys

class Commands:
    new = 'new'
    run = 'run'
    generate = 'gen'
    compile = 'compile'
    configure = 'config'
    switch = 'switch'
    show = 'show'
    remove = 'remove'
    reinstall = 'reinstall'


parser = argparse.ArgumentParser(prog="helper", description=f"contest-helper-{VERSION}")
subparsers = parser.add_subparsers(dest='command')

reinstall_parser = subparsers.add_parser(Commands.reinstall, description="reinstalls helper at the same directory")

new_parser = subparsers.add_parser(Commands.new, description="creates new environment")
new_parser.add_argument("name", help="name of the new environment")

switch_parser = subparsers.add_parser(Commands.switch, description="switches to test environment 'name'")
switch_parser.add_argument("name", help="name of the environment")

show_parser = subparsers.add_parser(Commands.show, description="shows information about current folder environments")
show_parser_group = show_parser.add_mutually_exclusive_group(required=True)
show_parser_group.add_argument('--all', help='all environments', action='store_true')
show_parser_group.add_argument('--current', help='current environments', action='store_true')

remove_parser = subparsers.add_parser(Commands.remove, description="removes the environment 'name'")
remove_parser.add_argument("name", help="name of the environment")

run_parser = subparsers.add_parser(Commands.run, description="executes tests")
run_parser_group = run_parser.add_mutually_exclusive_group(required=True)
run_parser_group.add_argument("-8", "--inf", help="generate and run tests forever", action="store_true")
run_parser_group.add_argument("--all", help="run all tests", action="store_true")
run_parser_group.add_argument("tests", help="tests to run", action="extend", nargs="*")

run_parser.add_argument("-t", "--timeout", help="timeout for tests", type=float, default=1)
run_parser.add_argument("-c", "--no-compile", help="doesn't compile before running tests", action="store_true")
run_parser.add_argument("-i", "--input", help="displays input", action="store_true")
run_parser.add_argument("-o", "--output", help="displays output", action="store_true")
run_parser.add_argument("-e", "--errors", help="displays errors", action="store_true")
run_parser.add_argument("-ce", "--checker-errors", help="displays checker output", action="store_true")
run_parser.add_argument("-co", "--checker-output", help="displays checker errors", action="store_true")

compile_parser = subparsers.add_parser(Commands.compile, description="compiles you program")

gen_parser = subparsers.add_parser(Commands.generate, description="generates tests")
gen_parser.add_argument("amount", type=int, help="amount of tests to generate")

edit_parser = subparsers.add_parser(Commands.configure, description="edit scripts")
edit_parser.add_argument("script", choices=('run', 'gen', 'compile', 'check'), help="edit scripts")

parsed_args = parser.parse_args(sys.argv[1:])

match parsed_args.command:
    case Commands.new:
        commands.new(parsed_args)
    case Commands.remove:
        commands.remove(parsed_args)
    case Commands.show:
        commands.show(parsed_args)
    case Commands.switch:
        commands.switch(parsed_args)
    case Commands.generate:
        commands.generate(parsed_args)
    case Commands.compile:
        commands.compile(parsed_args)
    case Commands.run:
        commands.run(parsed_args)
    case Commands.configure:
        commands.configure(parsed_args)
    case Commands.reinstall:
        commands.reinstall(parsed_args)
    case _:
        parser.print_help()