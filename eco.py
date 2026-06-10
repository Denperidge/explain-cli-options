#!/usr/bin/env python
from subprocess import run as _run  # runs --help or man
from argparse import ArgumentParser  # handles CLI
from re import search, MULTILINE, IGNORECASE  # searches --help/man
from sys import argv  # used to suggest re-running in a different mode if it has more results

DESCRIPTION = """

eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)

"""

debug = lambda x: x  # By default, don't log anything

"""
Args:
    - command: shell command to run
               for example: 'tar --help', 'man rsync'

Raises: if the command exits with any code that's not 0,
        it raises ChildProcessError containing stderr

Returns: utf-8 stdout
"""
def run(command: str) -> str:
    out = _run(command, shell=True, encoding="utf-8", capture_output=True)
    if out.returncode != 0:
        raise ChildProcessError(out.stderr)
    return out.stdout

"""
Wrapper arround run() that:
- Runs command with --help appended
- Returns stdout split by newline
"""
def get_help(command: str) -> list[str]:
    helpvar = run(f"{command} --help")
    return helpvar.split("\n")

"""
Wrapper arround run() that:
- Runs command with man prepended
- As opposed to get_help, catches ChildProcessError & returns []
  This ensures the script still works for people without man installed
- If it doesn't error, return stdout split by newline
"""
def get_man(command: str) -> list[str]:
    try:
        return run(f"man {command}").split("\n")
    except ChildProcessError:
        debug("Could not run man, returning empty list")
        return []

"""
Return all lines from haystack with regex-matched needle

If a line only has letters from needle in it,
an extra line is added to the output

Args:
    - haystack: list of lines
                for example: output from get_{man,help}
    - needle: string to search for in lines
                for example: '--progress', '-p', 'get-version'

Returns: list of lines matching the needle regex(es)
"""
def search_in_lines(haystack: list[str], needle: str) -> list[str]:
    regex_find_needle = fr"([^-\w]|^){needle}([^-]|$)"
    regex_letters_not_from_needle = fr"[^\W0-9{needle.replace("-", "")}]"
    debug(f"Searching help for {needle} with {regex_find_needle} & {regex_letters_not_from_needle}")
    
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
            if not search(pattern=regex_letters_not_from_needle, string=line, flags=IGNORECASE):
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


"""
Mode-independent part of searching command docs:
- Loops over individual args (['-pa', '--progress', 'get-version'])
- Splits up multiple shorthand args ('-pa' -> '-p', '-a')
- Run search_in_lines with individual args as needle
- Return results

Args:
    - lines: list of lines
             for example: output from get_{man,help}
    - command_args: list of arguments that need finding/explaining
                    for example: ['-av', '--progress', 'get-version'] 

Returns: list of relevant doc lines
"""
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

"""Supported modes"""
MODES = [
    { "name": "--help", "func": get_help },
    { "name": "man", "func": get_man }
]
"""Template for message in case the other mode has more results"""
STR_MORE_FOUND = ("More results were found in {0}. To search there, run:\n$ {1}")

"""
Mode-selected part of searching command docs:
- runs _get_relevant_command_docs using all modes
- if the selected mode has no results as opposed to the other,
  return results of functing using the other mode
- if the selected mode has results but less than the other,
  return message to notify user & show adapted eco usage
- if the selected mode has results,
  return found relevant lines

Args:
    - command: shell command to run
               for example: 'tar --help', 'man rsync'
    - selected_mode_name
    - command_args: list of arguments that need finding/explaining
                    for example: ['-av', '--progress', 'get-version'] 
    - second_try: if set to False, re-run again with
                  second_try = True and a different selected mode
                  if results are empty

Returns tuple (lines: list of relevant line str, message: None or string)
"""
def get_relevant_command_docs(command: str, selected_mode_name: str, command_args: list[str], second_try:bool=False) -> (list[str], str|None):
    out = {}
    message = None
    for mode in MODES:
        out[mode["name"]] = _get_relevant_command_docs(
            mode["func"](command), command_args)
    
    relevant_out = out[selected_mode_name]
    relevant_results = len(relevant_out)

    other_mode = "man" if selected_mode_name == "--help" else "--help"
    other_results = len(out[other_mode])

    if relevant_results < other_results:
        message = STR_MORE_FOUND.format("man pages", " ".join(argv))
        
    # If results were found in the current mode
    if relevant_results > 0:
        # But more are found in the other mode
        if other_results > relevant_results:
            # suggest re-running with different eco args to the user
            if other_mode == "--help":
                # If the better results came from --help,
                title = "--help output"
                # Remove +m/++man from re-run sugestion
                if "+m" in argv:
                    argv.remove("+m")
                if "++man" in argv:   # Don't use elif, remove both just in case
                    argv.remove("++man")
            elif other_mode == "man":
                # If the better results came from man,
                title = "man pages"
                argv.insert(1, "+m")  # Add +m to the re-run suggestion
            message = STR_MORE_FOUND.format(title, " ".join(argv))
        elif other_results == 0:
            # If no results can be found in any mode
            pass
    # If no relevant results found current mode but are found in other
    elif relevant_results == 0 and other_results > 0:
        debug(f"[MODE INFO] Couldn't find results using {selected_mode_name}, returning {other_mode} results...")
        return (out[other_mode], None)
    # If no results are found at all and there are still command args
    elif relevant_results == 0 and other_results == 0 and len(command_args) > 0:
        # Try again 
        if not second_try:
            command_args = [
                command + "-" + "-".join(command_args)
            ]
            return get_relevant_command_docs(command, selected_mode_name, command_args, second_try=True)


       

    
    return (relevant_out, message)

if __name__ == "__main__":
    # eco CLI handling
    parser = ArgumentParser(
        description=DESCRIPTION.strip(),
        prefix_chars="+")
    parser.add_argument("++debug", "+d", action="store_true", help="show debug output")
    parser.add_argument("++man", "+m", action="store_true", help="prioritise searching man contents over --help output")
    parser.add_argument("command", help="command which needs explaining (for example, tar)")
    parser.add_argument("args", nargs="+", help="args for the command you want explained (for example, -cvzf)")
    # TODO if no results try without spaces?
    args = parser.parse_args()

    # if debug is enabled, set debug to print
    if args.debug:
        debug = lambda x: print(x)

    # select mode
    mode = "man" if args.man else "--help"
    (lines, message) = get_relevant_command_docs(args.command, mode, args.args)
    
    # print found results
    for line in lines:
        print(line)
    
    # if more results are found in another mode, notify the user
    if message:
        print()
        print(message)


