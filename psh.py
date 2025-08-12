import os
import sys
aliases = {}
pshrc = os.path.expanduser("~/.pshrc")
if os.path.isfile(pshrc):
    try:
        with open(pshrc, "r") as f:
            exec(f.read())
    except Exception as e:
        print("Failed to read pshrc!")
    try:
        prompt_str = prompt
    except NameError:
        prompt_str = "psh prompt "
while True:
    choice = input(prompt_str)
    if os.name == "posix":
        clear_cmd = "clear"
    else:
        clear_cmd = "cls"
    parts = choice.split(maxsplit=1)
    cmd = parts[0]
    rest = parts[1] if len(parts) > 1 else ""

    if cmd in aliases:
        choice = aliases[cmd]
        if rest:
            choice += " " + rest
    if choice.lower() == "exit":
        print("Bye!")
        sys.exit()
    elif choice.lower() == "clear":
        os.system(clear_cmd)
    elif choice.startswith("cd"):
        parts = choice.split(maxsplit=1)
        if len(parts) == 1:
            directory = os.path.expanduser("~")
        else:
            directory = parts[1]
        try:
            os.chdir(directory)
        except FileNotFoundError:
            print("psh: cd: " + directory + ": No such file or directory")
        except NotADirectoryError:
            print("psh: cd: " + directory + ": Not a directory")
        except PermissionError:
            print("psh: cd: " + directory + ": Permission denied")
    elif choice.lower() == "pwd":
        print(os.getcwd())
    elif choice.startswith("run"):
        parts2 = choice.split(maxsplit=1)
        if len(parts2) == 1:
            print("psh: run: Filename required")
        else:
            filename = parts2[1]
            os.system(f"sh {filename}")
    elif choice.startswith("py "):
        code = choice[3:]
        try:
            exec(code)
        except Exception as e:
            print(f"Python error: {e}")
    else:
        os.system(choice)
