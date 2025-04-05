from argparse import ArgumentParser
from pathlib import Path
import sys
import os
import shutil

DIR_NAME = Path(".debug")

def init_global():
    if (not os.path.isdir(DIR_NAME)):
        os.mkdir(DIR_NAME)

def init(parsed: ArgumentParser):
    init_global()
    try:
        os.mkdir(DIR_NAME / parsed.name)
    except FileExistsError:
        print(f"Environment '{parsed.name}' already exists")
        sys.exit(1)
    except FileNotFoundError:
        print("Incorrect name of the environment")
        sys.exit(1)

def remove(parsed: ArgumentParser):
    try:
        shutil.rmtree(DIR_NAME / parsed.name)
    except OSError:
        print(f"An error occured. Sorry :(")
        sys.exit(1)

def list_all(parsed: ArgumentParser):
    print(*os.listdir(DIR_NAME), sep='\n')