# contest-helper
Helps poor MIPT students to solve contests

# Installation
```shell
git clone https://github.com/NNJunior/contest-helper.git
```
Then you want to create an alias to `python3 /path/to/contest-helper`. E.g. for `bash`:
```shell
echo "alias helper=\"python3 \\\"$(pwd)/contest-helper\\\"\"" >> ~/.bashrc
```
or for `zsh`:
```shell
echo "alias helper=\"python3 \\\"$(pwd)/contest-helper\\\"\"" >> ~/.zshrc
```

# Use of `helper`
You can always run `helper --help` to get some basic help over this tool.
## `helper new`
```
helper new [-h | --help] name
```
Creates new environment with in the current folder with name `<name>`.

## `helper show`
```
helper show [-h | --help] [--all | --current]
```
If flag `--all` is set, then shows all available environments for this directory, otherwise shows current environment.

## `helper switch`
```
helper switch [-h | --help] name
```
Allows you to switch between environments

## `helper remove`
```
helper remove [-h | --help] name
```
Allows you to remove environments

## `helper run`
```
helper run [-h] [-8] [--all] [-t TIMEOUT] [-c] [-i] [-o] [-e] [-ce] [-co] [tests ...]
```
Executes tests using `.debug/<environment>/scripts/run` scipt for each test

- flags `-8` or `--inf` is set if you want to run tests while your programm works correctly (incompatible with `--all` or with `[tests ...]`).
- flags `--all` is set if you want to run all available tests (incompatible with `-8` or `--inf` or with `[tests ...]`).
- `-t` or `--timeout` sets the timeout of your programm (default timeout is `1s`)
- `-c` or `--no-compile` is set when you don't want your code to be recompiled
- `-i` prints test body for each test
- `-o` prints output for each test
- `-e` prints errors for each test
- `-ce` prints checker errors for each test
- `-co` prints checker output for each test
- `[tests ...]` specifies which tests do you want to run (incompatible with `--all` or with `-8` or `--inf`).

## `helper compile`
```
helper compile [-h]
```
Compiles your code using `.debug/<environment>/scripts/compile` script

## `helper gen`
```
helper gen [-h] amount
```
Generates specified amount of tests at `.debug/<environment>/tests` script

## `helper config`
```
helper config [-h] script
```
Allows you to edit compile/run/generate/check scripts
