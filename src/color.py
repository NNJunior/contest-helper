import sys

def mark_red():
    print('\033[1;31m', end='')

def mark_green():
    print('\033[1;32m', end='')

def mark_purple():
    print('\033[1;35m', end='')

def mark_yellow():
    print('\033[1;33m', end='')


def clear_marks():
    print('\033[0m', end='')


def mark_error():
    mark_red()

def mark_info():
    mark_green()

def mark_warning():
    mark_purple()

def clear_marks():
    print('\033[0m', end='')

def print_error(*error, exit_code=1):
    mark_error()
    print('Error:', end=' ')
    clear_marks()
    print(*error)
    if exit_code is not None:
        sys.exit(exit_code)

def print_warning(*warning, exit_code=None):
    mark_warning()
    print('Warning:', end=' ')
    clear_marks()
    print(*warning)
    if exit_code is not None:
        sys.exit(exit_code)

def print_info(*info, exit_code=None):
    mark_info()
    print('Info:', end=' ')
    clear_marks()
    print(*info)
    if exit_code is not None:
        sys.exit(exit_code)
