#!/usr/bin/env python
from subprocess import run as _run
from argparse import ArgumentParser
from re import search, MULTILINE, IGNORECASE
from sys import argv

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
        debug("Could not run man, returning empty list")
        return []

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
            debug(f"\t[NON MATCH {needle}] '{line}'")

        # If the needle is in the line but not detected by regex, warn
        #elif needle in line:
        #    print(f"Possibly relevant, but not detected by regex:\n{line}")
        i += 1  # Move on to next line

    return relevant_lines

"""Mode-independent part of searching command docs"""
def _get_relevant_command_docs(lines: list[str], command_args:list[str]) -> list[str]:
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

MODES = [
    { "name": "--help", "func": get_help },
    { "name": "man", "func": get_man }
]
STR_MORE_FOUND = ("More results were found in {0}. To search there, run:\n$ {1}")
def get_relevant_command_docs(command: str, selected_mode_name: str, args: list[str], second_try:bool=False) -> (list[str], str|None):
    out = {}
    message = None
    for mode in MODES:
        out[mode["name"]] = _get_relevant_command_docs(
            mode["func"](command), args)
    
    relevant_out = out[selected_mode_name]
    relevant_results = len(relevant_out)

    if selected_mode_name == "--help" and len(out["man"]) > relevant_results:
    # If nothing was found, return results of man
        if relevant_results == 0 and not second_try:
            debug("[MODE INFO] Couldn't find results using --help, re-running with man...")
            return get_relevant_command_docs(command, "--help", args, second_try=True)

        # Else, just suggest re-running with different eco args to the user
        argv.insert(1, "+m")
        message = STR_MORE_FOUND.format("man pages", " ".join(argv))
    elif selected_mode_name == "man" and len(out["--help"]) > relevant_results:
        # If nothing was found, return results of --help
        if relevant_results == 0 and not second_try:
            debug("[MODE INFO] Couldn't find results using man, re-running with --help...")
            return get_relevant_command_docs(command, "--help", args, second_try=True)

        # Else, just suggest re-running with different eco args to the user
        if "+m" in argv:
            argv.remove("+m")
        if "++man" in argv:   # Don't use elif, remove both just in case
            argv.remove("++man")
        message = STR_MORE_FOUND.format("--help output", " ".join(argv))
    
    return (relevant_out, message)

if __name__ == "__main__":
    parser = ArgumentParser(
        description="eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)",
        prefix_chars="+")
    parser.add_argument("++debug", "+d", action="store_true", help="show debug output")
    parser.add_argument("++man", "+m", action="store_true", help="prioritise searching man contents over --help output")
    parser.add_argument("command", help="command which needs explaining (for example, tar)")
    parser.add_argument("args", nargs="+", help="args for the command you want explained (for example, -cvzf)")

    args = parser.parse_args()

    if args.debug:
        debug = lambda x: print(x)

    mode = "man" if args.man else "--help"
    (lines, message) = get_relevant_command_docs(args.command, mode, args.args)
    
    for line in lines:
        print(line)
    
    if message:
        print()
        print(message)


