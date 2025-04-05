import sys
import argparse
import commands

args = sys.argv[1:]

parser = argparse.ArgumentParser(prog="debug")
subparsers = parser.add_subparsers()

init_parser = subparsers.add_parser(commands.INIT, description="inititalizes new environment")
init_parser.add_argument("name", help="name of the new environment")

run_parser = subparsers.add_parser(commands.RUN, description="executes tests")
run_parser.add_argument("-8", "--inf", help="eenerate and run tests forever", action="store_true")
run_parser.add_argument("-t", "--timeout", help="timeout for tests", default=1)
run_parser.add_argument("-c", "--no-compile", help="doesn't compile before running tests", action="store_false")
run_parser.add_argument("-i", "--input", help="displays input", action="store_true")
run_parser.add_argument("-o", "--output", help="displays output", action="store_true")
run_parser.add_argument("-e", "--errors", help="displays errors", action="store_true")
run_parser.add_argument("-ce", "--checker-errors", help="displays checker output", action="store_true")
run_parser.add_argument("-co", "--checker-output", help="displays checker errors", action="store_true")
run_parser.add_argument("-T", "--tests", help="tests to run (defaults to all). Ignored when --inf or -8 is set", action="extend", nargs="+")

compile_parser = subparsers.add_parser(commands.COMPILE, description="compiles you program")

print(parser.parse_args(args))
