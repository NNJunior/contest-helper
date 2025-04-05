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
# First Steps
Helper is just a tool to test your code faster. Each program you want to test should be tested in different environment. For example, you want to test `main.cpp` - a program that adds up two numbers:
```cpp
#include <iostream>

int main() {
    int a;
    int b;
    std::cin >> a >> b;
    std::cout << a; // obvious mistake, will be fixed later
}
```

First, create environment to test it:
```shell
helper new main
```
Congratulations! You've just created environment with name `main`. Right now it's empty and is not suitable to test `main.cpp`. Let's fix that:

```
helper config compile
```
In opened editor, add line 
```
g++ /path/to/main.cpp
```
Now, let's set running script
```
helper config run
```
In opened editor, add line 
```
./a.out
```
Let's set out check script
```
helper config check
```
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3
In opened editor, add lines (replace `/path/to/python/interpteter` with the actual path to Python interpreter).
```python
#!/path/to/python/interpteter

a = int(input())
b = int(input())

with open('output.txt') as reader:
    answ = int(reader.read())
    if answ != a + b:
        raise Exception(f"expected '{a + b}', got '{answ}'")
```

Let's set out generate script
```
helper config gen
```
In opened editor, add lines (replace `/path/to/python/interpteter` with the actual path to Python interpreter).
```python
#!/path/to/python/interpteter

import random

print(random.randint(1, 100))
print(random.randint(1, 100))
```

Nice! We have set out environment to test `main.cpp`. Let's generate and run tests!
```shell
% helper gen 100
Info: Generated: test0.txt
Info: Generated: test1.txt
Info: Generated: test2.txt
            .
            .
            .
Info: Generated: test99.txt

% helper run --all
Info: Compiling...
Info: Compilation successfull!
Info: Running tests...
test0.txt   WA  0.001s
test1.txt   WA  0.001s
    .
    .
    .
test99.txt   WA  0.001s
```
Whoops, looks like our programm fails. Let's check its output:
```
% helper run test0.txt -ce
Info: Compiling...
Info: Compilation successfull!
Info: Running tests...
test0.txt       WA      0.658489s
checker errors:
Traceback (most recent call last):
  File "path/to/.debug/main/scripts/check", line 9, in <module>
    raise Exception(f"expected '{a + b}', got '{answ}'")
Exception: expected '146', got '50'
```
Let's correct the mistake that was made in `main.cpp`:
```cpp
#include <iostream>

int main() {
    int a;
    int b;
    std::cin >> a >> b;
    std::cout << a + b;
}
```
And rerun `helper run --all` to check if we've forgotten something:
```
% helper run --all
Info: Compiling...
Info: Compilation successfull!
Info: Running tests...
test0.txt   OK  0.001s
test1.txt   OK  0.001s
    .
    .
    .
test99.txt   OK  0.001s
```
Fine! Now you can use `helper`!

# `helper` functionality
You can always run `helper --help` to get some basic help over this tool.
## `helper --version`
Shows the version of `helper`

## `helper new`
```
helper new [-h | --help] name
```
Creates new environment with in the current folder with name `<name>`. When an envrionment is created, it is not set to test your code. See `helper config` for configuring compile/run/generate/check scripts. 

## `helper reinstall`
```
helper reinstall [-h | --help]
```
Reinstalls `helper` at the same directory

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
