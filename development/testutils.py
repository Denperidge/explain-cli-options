from subprocess import run as _run

def run(command: str):
    out = _run(command, shell=True, encoding="utf-8", capture_output=True)
    if out.returncode != 0:
        raise Exception(out.stderr)
    return out.stdout

def eco(command: str):
    return run("../eco.py " + command)

def get_help(command: str):
    return run(command + " --help")

def get_index_from_help(command: str, needle: str):
    help_out = get_help(command).split("\n")
    i = 0
    for line in help_out:
        if needle in line:
            return i
        i+=1


EXPECTED_MORE_FOUND = """
More results were found in man pages. To search there, run:
$ ../eco.py {0}{1}
"""
def more_found(expected: str, command: str, man=False):
    return expected + EXPECTED_MORE_FOUND.format(
        "" if not man else "+m ", command)

# man --all passwd | cat