from subprocess import run as _run
from typing import Literal

def run(command: str):
    out = _run(command, shell=True, encoding="utf-8", capture_output=True)
    if out.returncode != 0:
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
def get_index_from(command: str, needle: str):
    needle = needle.strip()
    output = run(command).split("\n")
    i = 0
    for line in output:
        if needle in line:
            return i
        i+=1
    #raise ValueError(f"Needle {needle} not found in {command}. output: {output}")

def get_index_from_help(command: str, needle: str):
    return get_index_from(command + " --help", needle)

def get_index_from_man(command: str, needle: str):
    return get_index_from("man " + command.split(" ")[0], needle)  # TODO: cleaner version than command split


def equal_or_assertionerror(returned: str, expected: str):
    if returned == expected:
        return True
    else:
        raise AssertionError(f"\n'{returned}'\n(returned value) does not equal expected value\n'{expected}'")




# EXPECTED_MORE_FOUND = """
# More results were found in man pages. To search there, run:
# $ ../eco.py {0}{1}{2}
# """
# def more_found(command: str, expected: str, no_index=False):
#     return expected + EXPECTED_MORE_FOUND.format(
#         "" if not no_index else "++no-index ",
#         "" if "+m" in command else "", command)
#

EXPECTED_MORE_FOUND = """
More results were found in man pages. To search there, run:
$ ../eco.py {0}{1}
"""
def more_found(expected: str, command: str, man=False):
    return expected + EXPECTED_MORE_FOUND.format(
        "" if not man else "+m ", command)
