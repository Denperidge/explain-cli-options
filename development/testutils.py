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

def equal_or_assertionerror(returned: str, expected: str):
    if returned == expected:
        return True
    else:
        raise AssertionError(f"'{returned}'\n(returned value) does not equal expected value\n{expected}'")


"""
Assert that a command returns the expected result with and without ++no-index 
"""
def eco_returns(command: str, expected: str) -> bool:
    # First compare with ++no-index
    # Original default, expecteds are written without line indexes
    assert equal_or_assertionerror(eco("++no-index " + command), expected)

    # New default, as this is more informational with little clutter
    returned_lines: list[str] = eco(command).split("\n")

    # Transform expected lines to add line index
    expected_lines: list[str] = expected.split("\n")
    for i in range(0, len(expected_lines)):
        line = expected_lines[i]
        line_index = get_index_from_help(command, line)
        expected_lines[i] = f"[{line_index}] {line}"
    
    # Compare lines
    for i in range(0, len(returned_lines)):
        returned_line = returned_lines[i]
        expected_line = expected_lines[i]
        
        if expected_line == "[0] " and returned_line == "":
            continue

        # Ensure first character is the index bracket
        assert equal_or_assertionerror(returned_line[0], "[")
        assert equal_or_assertionerror(expected_line[0], "[")

        assert equal_or_assertionerror(returned_line, expected_line)

    # If this part is reached, all assertions succeeded
    return True


EXPECTED_MORE_FOUND = """
More results were found in man pages. To search there, run:
$ ../eco.py {0}{1}
"""
def more_found(expected: str, command: str, man=False):
    return expected + EXPECTED_MORE_FOUND.format(
        "" if not man else "+m ", command)

# man --all passwd | cat
