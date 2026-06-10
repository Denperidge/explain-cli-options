from subprocess import run
def eco(command: str):
    out = run("../eco.py " + command, shell=True, encoding="utf-8", capture_output=True)
    if out.returncode != 0:
        raise Exception(out.stderr)
    return out.stdout

EXPECTED_MORE_FOUND = """
More results were found in man pages. To search there, run:
$ ../eco.py {0}{1}
"""
def more_found(expected: str, command: str, man=False):
    return expected + EXPECTED_MORE_FOUND.format(
        "" if not man else "+m ", command)

# man --all passwd | cat