#!/usr/bin/env python
from subprocess import run as _run
from argparse import ArgumentParser
from re import search, MULTILINE

def run(command: str, capture_output=True):
    out = _run(command, shell=True, encoding="utf-8", capture_output=capture_output)
    if out.returncode != 0:
        raise Exception(out.stderr)
    return out.stdout

def get_help(command: str) -> list[str]:
    helpvar = run(f"{command} --help")
    return helpvar.split("\n")

def search_help(helplines: list[str], needle: str) -> list[str]:
    return list(filter(lambda line: search(pattern=fr"([^-\w]|^){needle}[^-]", flags=MULTILINE, string=line), helplines))

def parse_help(command: str, command_args:list[str]):
    helpvar = get_help(command)
    to_print = []
    for arg in command_args:
        # e.g. --progress or status
        if arg.startswith("--") or not arg.startswith("-"):
            to_print += search_help(helpvar, arg)
        elif arg.startswith("-"):
            if len(arg) == 2:  # e.g. -d
                to_print += search_help(helpvar, arg)
            else:  # e.g. -xvz
                needles = list(arg)
                needles.remove("-")
                for needle in needles:
                    to_print += search_help(helpvar, f"-{needle}")
        else:
            print(f"Skipping non-option: {arg}")
    return to_print


if __name__ == "__main__":
    parser = ArgumentParser(
        description="eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)",
        prefix_chars="+")
    parser.add_argument("command", help="command which needs explaining (for example, tar)")
    parser.add_argument("args", nargs="+", help="args for the command you want explained (for example, -cvzf)")

    args = parser.parse_args()

    for line in parse_help(args.command, args.args):
        print(line)


