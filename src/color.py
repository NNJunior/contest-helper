import sys

def mark_error():
    print('\033[1;31m', end='')

def mark_info():
    print('\033[1;32m', end='')

def mark_warning():
    print('\033[1;35m', end='')

def clear_marks():
    print('\033[0m', end='')

def print_error(error: str, exit_code=1):
    mark_error()
    print('Error:', end=' ')
    clear_marks()
    print(error)
    if exit_code is not None:
        sys.exit(exit_code)

def print_warning(warning: str, exit_code=None):
    mark_warning()
    print('Warning:', end=' ')
    clear_marks()
    print(warning)
    if exit_code is not None:
        sys.exit(exit_code)

def print_info(info: str, exit_code=None):
    mark_info()
    print('Info:', end=' ')
    clear_marks()
    print(info)
    if exit_code is not None:
        sys.exit(exit_code)
