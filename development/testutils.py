from subprocess import run as _run
from typing import Literal
from re import  sub, finditer, match

from re import MULTILINE
REGEX_NO_QUOTES = r"""^(?P<one>['"]).+?(?P<two>['"])"""


"""

Input: 'cargo add' --dev --help
Output: cargo add --dev --help

Input: cargo 'add dev' --help
Output: cargo 'add dev' --help
"""
def clean_first_quotes(string: str):
    regexmatch = match(REGEX_NO_QUOTES, string, MULTILINE)
    if not regexmatch:
        return string
    else:
        span = list(regexmatch.span())
        span[1] -= 2  # The first quote will be removed first
        for index in span:
            string = string[0:index] + string[index+1:]
        return string


def run(command: str):
    out = _run(clean_first_quotes(command), shell=True, encoding="utf-8", capture_output=True)
    if out.returncode == 16 and command.startswith("man"):
        pass  # man cargo -v  returns this, for example
    elif out.returncode != 0:
        raise Exception(out.stderr)
    return out.stdout

"""
Run eco with ++no-index for future proofing
"""
def eco(command: str):
    return run("../eco.py " + command)

def get_help(command: str):
    return run(command + " --help")

"""
Other versions of dependencies have different indexes
this broke CI on GitHub Actions/ubuntu-latest
Use a search instead
"""
def get_index_from(command: str, needle: str, man:bool=False):
    command = clean_first_quotes(command)
    commands = command.split(" ")

    # First look in base command. Otherwise,
    for i in range(1, len(commands) ):
        command = " ".join(commands[0:i])
        if man:
            command = "man " + command
        else:
            command += " --help"

        output = run(command).split("\n")
        i = 0
        for line in output:
            if needle in line:
                return i
            i+=1
    #raise ValueError(f"Needle {needle} not found in {command}. output: {output}")

def get_index_from_help(command: str, needle: str):
    return get_index_from(command, needle, False)

def get_index_from_man(command: str, needle: str):
    return get_index_from(command, needle, True)


def equal_or_assertionerror(returned: str, expected: str):
    if returned == expected:
        return True
    else:
        raise AssertionError(f"\n'{returned}'\n(returned value) does not equal expected value\n'{expected}'")






# EXPECTED_MORE_FOUND = """
# More results were found in man pages. To search there, run:
# $ ../eco.py {0}++no-index {1}
# """
# def more_found(expected: str, command: str, with_index:bool=False, man:bool=False):
#     return expected + EXPECTED_MORE_FOUND.format(
#         "" if not man else "+m ", command.replace("'", ""))  # TODO cleaner solution than replace
#
EXPECTED_MORE_FOUND = """
More results were found in man pages. To search there, run:
$ ../eco.py {0}{1}{2}
"""
def more_found(command: str, expected: str, no_index:bool=False, man: bool=False):
    return expected + EXPECTED_MORE_FOUND.format(
        "" if not man else "+m ",
        "" if not no_index else "++no-index ",
        clean_first_quotes(command))

from tests import MoreFoundIn
def add_more_found_if_needed(command: str, expected: str, no_index:bool, more_found_in: MoreFoundIn):
    if more_found_in != "N/A":
        expected = more_found(command, expected, no_index, False if more_found_in == "More found in help" else True)
    return expected



