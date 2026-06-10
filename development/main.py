from argparse import ArgumentParser
from sys import path, argv
path.append("../")
from eco import run, get_help

ENCODING = "utf-8"


def generate_readme():
    with open("template.README.md", mode="r", encoding=ENCODING) as file:
        template = file.read()
    
    vermin_out = run("vermin ../eco.py").split("\n")
    version = list(filter(lambda line: line.startswith("Minimum"), vermin_out))[0]
    version = version.replace("versions", "Python version")

    usage = ""
    usage_examples = ["rsync -a", "rsync -rlptgoD --progress"]
    for example in usage_examples:
        usage += "$ eco " + example + "\n"
        usage += run("../eco.py " + example)
        usage += "\n"

    out = template\
        .replace("{vermin}", version)\
        .replace("{help}", run("../eco.py ++help"))\
        .replace("{usage}", usage.rstrip())
    
    with open("../README.md", mode="w", encoding=ENCODING) as file:
        file.write(out)

def relaunch_with_uv_and_exit():
    from pathlib import Path

    if not Path(".venv").exists():
        run("uv venv")
        print("Generated .venv")
    
    uv_version = "uv run " + " ".join(argv)
    print("[RELAUNCH AS] " + uv_version)
    print(run(uv_version))
    exit(0)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--readme", "-r", action="store_true", help="Generate README")
    parser.add_argument("--test", "-t", action="store_true", help="Run tests")

    args = parser.parse_args()
    
    readme = args.readme
    test = args.test

    if not readme and not test:
        parser.print_help()
    
    if readme:
        generate_readme()
    
    if test:
        # Support for uv run main.py -t & python main.py -t
        print("Testing. Checking if pytest is installed...")
        try: 
            import pytest
            run("uv run pytest", capture_output=False)
        except ModuleNotFoundError:
            print("Pytest not installed. Creating and/or loading venv & restarting...")
            relaunch_with_uv_and_exit()
        



