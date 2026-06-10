#!/usr/bin/env python
from subprocess import run as _run
from argparse import ArgumentParser
from re import search, MULTILINE, IGNORECASE

debug = lambda x: x

def run(command: str, capture_output=True) -> str:
    out = _run(command, shell=True, encoding="utf-8", capture_output=capture_output)
    if out.returncode != 0:
        raise ChildProcessError(out.stderr)
    return out.stdout

def get_help(command: str) -> list[str]:
    helpvar = run(f"{command} --help")
    return helpvar.split("\n")

def get_man(command: str) -> list[str]:
    try:
        return run(f"man {command}").split("\n")
    except ChildProcessError:
        debug("Could not run man")
        return False

def search_in_lines(haystack: list[str], needle: str) -> list[str]:
    regex_find_needle = fr"([^-\w]|^){needle}([^-]|$)"
    regex_letters_not_From_needle = fr"[^\W{needle.replace("-", "")}]"
    debug(f"Searching help for {needle} with {regex_find_needle} & {regex_letters_not_From_needle}")
    
    relevant_lines = []
    i = 0  # while instead of for so index can be increased
    while i != len(haystack):
        line = haystack[i]
        # If regex can find needle in line
        if search(pattern=regex_find_needle, string=line, flags=MULTILINE):
            debug(f"\t[MATCH {needle}] {line}")
            # Return it
            relevant_lines.append(line)
            
            debug(f"\t[MATCH {needle}] checking if only {needle} letters are in line")
            # If the line only has word characters that are in the needle
            if not search(pattern=regex_letters_not_From_needle, string=line, flags=IGNORECASE):
                debug(f"\t[EMPTY] no letters aside from {needle} letters are in line. Adding extra line...")
                
                i += 1  # Move index up
                relevant_lines.append(haystack[i])  # Add next line
        else:
            debug(f"\t[NON MATCH {needle}] {line}")

        # If the needle is in the line but not detected by regex, warn
        #elif needle in line:
        #    print(f"Possibly relevant, but not detected by regex:\n{line}")
        i += 1  # Move on to next line

    return relevant_lines

def get_relevant_command_docs(command: str, command_args:list[str]) -> list[str]:
    lines = get_help(command) # get_man(command) or get_help(command)
    to_print = []
    for arg in command_args:
        # e.g. --progress or status
        if arg.startswith("--") or not arg.startswith("-"):
            to_print += search_in_lines(lines, arg)
        elif arg.startswith("-"):
            if len(arg) == 2:  # e.g. -d
                to_print += search_in_lines(lines, arg)
            else:  # e.g. -xvz
                needles = list(arg)
                needles.remove("-")
                for needle in needles:
                    to_print += search_in_lines(lines, f"-{needle}")
        else:
            print(f"Skipping non-option: {arg}")
    return to_print


if __name__ == "__main__":
    parser = ArgumentParser(
        description="eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)",
        prefix_chars="+")
    parser.add_argument("++debug", "+d", action="store_true", help="show debug output")
    parser.add_argument("command", help="command which needs explaining (for example, tar)")
    parser.add_argument("args", nargs="+", help="args for the command you want explained (for example, -cvzf)")

    args = parser.parse_args()

    if args.debug:
        debug = lambda x: print(x)
    
    for line in get_relevant_command_docs(args.command, args.args):
        print(line)


