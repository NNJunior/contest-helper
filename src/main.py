import argparse
import commands
import sys

class Commands:
    init = 'init'
    run = 'run'
    generate = 'gen'
    compile = 'compile'
    edit = 'edit'
    switch = 'switch'
    list = 'list'
    remove = 'remove'


parser = argparse.ArgumentParser(prog="debug")
subparsers = parser.add_subparsers(dest='command')

init_parser = subparsers.add_parser(Commands.init, description="inititalizes new environment")
init_parser.add_argument("name", help="name of the new environment")

init_parser = subparsers.add_parser(Commands.switch, description="switches to test environment 'name'")
init_parser.add_argument("name", help="name of the environment")

init_parser = subparsers.add_parser(Commands.list, description="shows all environments available in this folder")

init_parser = subparsers.add_parser(Commands.remove, description="removes the environment 'name'")
init_parser.add_argument("name", help="name of the environment")

run_parser = subparsers.add_parser(Commands.run, description="executes tests")
run_parser.add_argument("-8", "--inf", help="generate and run tests forever", action="store_true")
run_parser.add_argument("-t", "--timeout", help="timeout for tests", type=float, default=1)
run_parser.add_argument("-c", "--no-compile", help="doesn't compile before running tests", action="store_true")
run_parser.add_argument("-i", "--input", help="displays input", action="store_true")
run_parser.add_argument("-o", "--output", help="displays output", action="store_true")
run_parser.add_argument("-e", "--errors", help="displays errors", action="store_true")
run_parser.add_argument("-ce", "--checker-errors", help="displays checker output", action="store_true")
run_parser.add_argument("-co", "--checker-output", help="displays checker errors", action="store_true")
run_parser.add_argument("-T", "--tests", help="tests to run (defaults to all). Ignored when --inf or -8 is set", action="extend", nargs="+")

compile_parser = subparsers.add_parser(Commands.compile, description="compiles you program")

gen_parser = subparsers.add_parser(Commands.generate, description="generates tests")
gen_parser.add_argument("amount", type=int, help="amount of tests to generate")

edit_parser = subparsers.add_parser(Commands.edit, description="edit scripts")
edit_parser.add_argument("script", choices=('run', 'gen', 'compile', 'check'), help="edit scripts")

parsed_args = parser.parse_args(sys.argv[1:])

match parsed_args.command:
    case Commands.init:
        commands.init(parsed_args)
    case Commands.remove:
        commands.remove(parsed_args)
    case Commands.list:
        commands.list_all(parsed_args)