from math import exp
from subprocess import run as _run

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
def get_index_from_help(command: str, needle: str):
    help_out = get_help(command).split("\n")
    i = 0
    for line in help_out:
        if needle in line:
            return i
        i+=1


"""

"""
def eco_returns(command: str, expected: str, without_line_index: bool=False) -> bool:
    returned: str = eco(command)
    if without_line_index:
        # Original default, expecteds are written without line indexes
        return returned == expected
    else:
        # New default, as this is more informational with little clutter
        returned_lines: list[str] = returned.split("\n")
        expected_lines: list[str] = expected.split("\n")
        for i in range(0, len(expected_lines)):
            line = expected_lines[i]
            line_index = get_index_from_help(command, line)
            expected_lines[i] = f"[{line_index}] {line}"

        
        for i in range(0, len(returned_lines)):
            returned_line = returned_lines[i]
            expected_line = expected_lines[i]


            if expected_line == "[0] " and returned_line == "":
                continue
            if expected_line != returned_line:
                raise AssertionError(f"'{expected_line}'\nEXPECTED DOES NOT EQUAL RETURNED\n'{returned_line}'")
        return True



    


EXPECTED_MORE_FOUND = """
More results were found in man pages. To search there, run:
$ ../eco.py {0}{1}
"""
def more_found(expected: str, command: str, man=False):
    return expected + EXPECTED_MORE_FOUND.format(
        "" if not man else "+m ", command)

# man --all passwd | cat
