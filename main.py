import sys
import argparse
import commands

args = sys.argv[1:]

parser = argparse.ArgumentParser(prog='debug')
subparsers = parser.add_subparsers()

init_parser = subparsers.add_parser(commands.INIT, description="inititalizes new environment")
init_parser.add_argument('name', help="name of the new environment")

run_parser = subparsers.add_parser(commands.RUN, description="executes tests")
run_parser.add_argument('-8', '--inf', help="Generate and run tests forever", action='store_true')
run_parser.add_argument('-t', '--timeout', help="timeout for tests", default=1)
run_parser.add_argument('-i', '--input', help="Displays input", action='store_true')
run_parser.add_argument('-o', '--output', help="Displays output", action='store_true')
run_parser.add_argument('-e', '--errors', help="Displays errors", action='store_true')
run_parser.add_argument('-ce', '--checker-errors', help="Displays checker output", action='store_true')
run_parser.add_argument('-co', '--checker-output', help="Displays checker errors", action='store_true')
run_parser.add_argument('--tests', help="Tests to run (default all). Ignored when --inf or -8 is set", action='extend', nargs='+')
print(parser.parse_args(args))